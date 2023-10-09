import requests

def init_problem(alg_name, bin_size):
    return requests.get(f"http://{alg_name}:5000/newproblem/{bin_size}").json()['problemID']

def do_requests(alg_name, problem_id, items):
    for item in items:
        requests.get(f"http://{alg_name}:5000/placeitem/{problem_id}/{item}")

def get_results(alg_name, problem_id, bin_size):
    result = requests.get(f"http://{alg_name}:5000/endproblem/{problem_id}").json()
    num_bins = result['count']
    efficiency = result['size'] / (num_bins * bin_size)
    return num_bins, efficiency

def run_test(alg_name, bin_size, case):
    id = init_problem(alg_name, bin_size)
    do_requests(alg_name, id, case)
    bins, efficiency = get_results(alg_name, id, bin_size)
    return bins, efficiency
    
def evaluate_algorithm(alg_name, bin_size, cases):
    results = {'bins': [], 'efficiency': []}
    for case in cases:
        bins, efficiency = run_test(alg_name, bin_size, case)
        results['bins'].append(bins)
        results['efficiency'].append(efficiency)
    return results

def calculate_alg_stats(results):
    stats = {}
    stats['avg_bins'] = sum(results['bins']) / len(results['bins'])
    stats['avg_efficiency'] = sum(results['efficiency']) / len(results['efficiency'])
    return stats

def calculate_stats(results):
    stats = {}
    for alg_name in results:
        stats[alg_name] = calculate_alg_stats(results[alg_name])
    return stats


def compare_algorithms(alg_names, bin_size):
    results = {}
    cases = requests.get(f"http://storage:5000/getcases/{bin_size}").json()['cases']
    for alg_name in alg_names:
        results[alg_name] = evaluate_algorithm(alg_name, bin_size, cases)
    
    stats = calculate_stats(results)
    return stats