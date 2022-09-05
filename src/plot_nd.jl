using Plots
using Random: GLOBAL_RNG
using RandomExtensions

@inline function dist2(a, b)
    return sum((ai - bi)^2 for (ai, bi) in zip(a, b))
end

@inline function dist2(a, b::Float64)
    return sum((ai - b)^2 for ai in a)
end

function sample_nd_plot(rng, shape, desired_samples; max_retry_times=100)
    p = scatter(leg=false, xlims=(0, shape[1]), ylims=(0, shape[2]), zlims=(0, shape[3]))
    anim = Animation()
    D = length(shape)
    T = NTuple{D,Float64}
    R = √D
    M = Int(ceil(R))
    grid = fill(-1, shape...)
    start_cell = (((shape[d] + 1) ÷ 2 for d in 1:D)...,)
    first_sample = ((0.5 * shape[d] for d in 1:D)...,)
    samples = [first_sample]
    grid[start_cell...] = 1
    sizehint!(samples, desired_samples)
    head = 1
    while head <= length(samples) < desired_samples
        for _ in 1:max_retry_times
            r = rand(rng, T)
            while dist2(r, 0.5) < 0.0625 || dist2(r, 0.5) > 0.25
                r = rand(rng, T)
            end
            r′ = ((xi + (dxi - 0.5) * 4R for (xi, dxi) in zip(samples[head], r))...,)
            if all(0 <= x <= sx for (x, sx) in zip(r′, shape))
                pos = ((Int(ceil(xi′)) for xi′ in r′)...,)
                index = CartesianIndex(pos)
                if grid[index] == -1
                    collision = false
                    for neighbor in CartesianIndices(((max(1, id - M):min(sd, id + M) for (id, sd) in zip(pos, shape))...,))
                        if grid[neighbor] != -1 && dist2(r′, samples[grid[neighbor]]) < R^2
                            collision = true
                            break
                        end
                    end
                    if !collision
                        push!(samples, r′)
                        grid[index] = length(samples)
                        if length(samples) % 100 == 0
                            scatter!(p, [x[1] for x in samples[end-99:end]], [x[2] for x in samples[end-99:end]], [x[3] for x in samples[end-99:end]], markersize=0.2)
                            frame(anim)
                        end
                        if length(samples) == desired_samples
                            return anim
                        end
                    end
                end
            end
        end
        head += 1
    end

    return anim
end

sample_nd_plot(shape, desired_samples) = sample_nd_plot(GLOBAL_RNG, shape, desired_samples)

anim = sample_nd_plot((100, 100, 100), 10000)
gif(anim, "poisson_nd.gif")
