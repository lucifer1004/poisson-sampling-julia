using Random: GLOBAL_RNG

function sample_2d(rng, shape, desired_samples; max_retry_times=100)
    R = √2
    grid = fill(-1, shape...)
    start_cell = ((shape[1] + 1) ÷ 2, (shape[2] + 1) ÷ 2)
    first_sample = (shape[1] * 0.5, shape[2] * 0.5)
    samples = [first_sample]
    grid[start_cell...] = 1
    sizehint!(samples, desired_samples)
    head = 1
    while head <= length(samples) < desired_samples
        for _ in 1:max_retry_times
            x, y = rand(rng) - 0.5, rand(rng) - 0.5
            while x^2 + y^2 < 0.0625 || x^2 + y^2 > 0.25
                x, y = rand(rng) - 0.5, rand(rng) - 0.5
            end
            x′, y′ = samples[head][1] + x * 4R, samples[head][2] + y * 4R
            if 0 <= x′ <= shape[1] && 0 <= y′ <= shape[2]
                px, py = Int(ceil(x′)), Int(ceil(y′))
                index = CartesianIndex((px, py))
                if grid[index] == -1
                    collision = false
                    for j in max(1, py - 2):min(shape[2], py + 2)
                        for i in max(1, px - 2):min(shape[1], px + 2)
                            if grid[i, j] != -1
                                nx, ny = samples[grid[i, j]]
                                if (nx - x′)^2 + (ny - y′)^2 < R^2
                                    collision = true
                                    break
                                end
                            end
                        end
                        if collision
                            break
                        end
                    end
                    if !collision
                        push!(samples, (x′, y′))
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

sample_2d(shape, desired_samples) = sample_2d(GLOBAL_RNG, shape, desired_samples)
