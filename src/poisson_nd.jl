using Random: GLOBAL_RNG
using RandomExtensions

@inline function dist2(a, b)
    return sum((ai - bi)^2 for (ai, bi) in zip(a, b))
end

@inline function dist2(a, b::Float64)
    return sum((ai - b)^2 for ai in a)
end

function sample_nd(rng, shape, desired_samples; max_retry_times=100)
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
                        if length(samples) == desired_samples
                            return samples
                        end
                    end
                end
            end
        end
        head += 1
    end

    return samples
end

sample_nd(shape, desired_samples) = sample_nd(GLOBAL_RNG, shape, desired_samples)
