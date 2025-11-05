import numpy as np

def fitness_function(position):
    """Hàm mục tiêu: f(x, y, z) = x² + y² + z²"""
    return np.sum(position**2)

def scso(num_iterations, num_agents=3, dim=3, lb=-10, ub=10, SM=2):
    # Khởi tạo quần thể
    population = np.random.uniform(lb, ub, (num_agents, dim))
    fitness = np.array([fitness_function(agent) for agent in population])

    # Tìm cá thể tốt nhất ban đầu
    best_idx = np.argmin(fitness)
    best_agent = population[best_idx].copy()
    best_fitness = fitness[best_idx]

    for it in range(num_iterations):
        rG = SM * (1 - it / num_iterations)  # Eq. (1)
        R = 2 * rG * np.random.rand() - rG    # Eq. (2)

        for i in range(num_agents):
            r = rG * np.random.rand()        # Eq. (3)
            theta_deg = np.random.uniform(0, 360)
            theta = np.radians(theta_deg)    # Roulette-based angle

            if abs(R) > 1:  # Exploration phase (Eq. 4)
                rand_factor = np.random.rand()
                new_position = r * abs(best_agent - rand_factor * population[i])
            else:           # Exploitation phase (Eq. 5 + Eq. 6)
                posrnd = np.abs(np.random.rand() * best_agent - population[i])  # Eq. (5)
                new_position = best_agent - r * posrnd * np.cos(theta)          # Eq. (6)

            # Ràng buộc trong khoảng [lb, ub]
            new_position = np.clip(new_position, lb, ub)
            new_fitness = fitness_function(new_position)

            # Cập nhật nếu tốt hơn
            if new_fitness < fitness[i]:
                population[i] = new_position
                fitness[i] = new_fitness

                if new_fitness < best_fitness:
                    best_agent = new_position.copy()
                    best_fitness = new_fitness

        print(f"Iter {it+1:02d}: Best Fitness = {best_fitness:.6f}, Best Pos = {best_agent}")

        for idx in range(num_agents):
            print(f"Mèo {idx+1}: Pos = {population[idx]}  ")

    return best_agent, best_fitness

best_solution, best_value = scso(num_iterations=30)
print("\n✅ Final Best Solution:", best_solution)
print("✅ Final Best Fitness:", best_value)