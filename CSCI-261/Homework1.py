import random
import time

# CSCI-261 Homework 1 problem four
# Time complexity and ratios for insertion sort and counting sort

insertion_count = 0
counting_count = 0
results = []


def insertion_sort(A, count_ops=False):
    global insertion_count

    for j in range(1, len(A)):
        key = A[j]
        i = j - 1

        if count_ops:
            insertion_count += 2

        while i >= 0:
            if count_ops:
                insertion_count += 1

            if A[i] <= key:
                if count_ops:
                    insertion_count += 1
                break

            if count_ops:
                insertion_count += 1

            A[i + 1] = A[i]
            i -= 1

            if count_ops:
                insertion_count += 2

        A[i + 1] = key

        if count_ops:
            insertion_count += 1

    return A


def counting_sort(A, k, count_ops=False):
    global counting_count

    B = [0] * len(A)
    C = [0] * (k + 1)

    if count_ops:
        counting_count += 2

    for i in range(k + 1):
        C[i] = 0

        if count_ops:
            counting_count += 1

    for j in range(len(A)):
        C[A[j]] += 1

        if count_ops:
            counting_count += 1

    for i in range(1, k + 1):
        C[i] += C[i - 1]

        if count_ops:
            counting_count += 1

    for j in range(len(A) - 1, -1, -1):
        B[C[A[j]] - 1] = A[j]
        C[A[j]] -= 1

        if count_ops:
            counting_count += 2

    return B


def make_random_data(n, k): # Helper function so I dont have to manually create random data each time
    return [random.randint(0, k) for _ in range(n)]


def get_data_types(data):
    sorted_data = sorted(data)

    return {
        "Random": data.copy(),
        "Sorted": sorted_data,
        "Reverse": sorted_data[::-1]
    }


def time_insertion(data):
    test = data.copy()

    start = time.perf_counter()
    insertion_sort(test)
    end = time.perf_counter()

    return end - start


def time_counting(data, k):
    test = data.copy()

    start = time.perf_counter()
    counting_sort(test, k)
    end = time.perf_counter()

    return end - start


def get_insertion_count(data):
    global insertion_count

    insertion_count = 0
    insertion_sort(data.copy(), True)

    return insertion_count


def get_counting_count(data, k):
    global counting_count

    counting_count = 0
    counting_sort(data.copy(), k, True)

    return counting_count


def run_test(n, k, range_name):
    data = make_random_data(n, k)
    data_types = get_data_types(data)

    for data_name, current_data in data_types.items():

        insertion_time = time_insertion(current_data)
        insertion_ops = get_insertion_count(current_data)

        counting_time = time_counting(current_data, k)
        counting_ops = get_counting_count(current_data, k)

        results.append({
            "n": n,
            "range": range_name,
            "data": data_name,
            "insertion_time": insertion_time,
            "insertion_ops": insertion_ops,
            "counting_time": counting_time,
            "counting_ops": counting_ops
        })

        print("\n", range_name, "-", data_name, "- n =", n)

        print("Insertion Sort")
        print("  Time:", insertion_time)
        print("  Count:", insertion_ops)

        print("Counting Sort")
        print("  Time:", counting_time)
        print("  Count:", counting_ops)


def find_result(n, range_name, data_name):
    for result in results:
        if (
            result["n"] == n
            and result["range"] == range_name
            and result["data"] == data_name
        ):
            return result

    return None


def print_ratios():
    sizes = [64, 256, 1024, 4096]
    ranges = ["8n", "n^2"]
    data_types = ["Random", "Sorted", "Reverse"]

    print("\n\nRATIOS")
    print("=" * 70)

    for range_name in ranges:
        for data_name in data_types:

            print("\nRange:", range_name)
            print("Data:", data_name)

            for i in range(1, len(sizes)):
                old_n = sizes[i - 1]
                new_n = sizes[i]

                old = find_result(old_n, range_name, data_name)
                new = find_result(new_n, range_name, data_name)

                insertion_time_ratio = (
                    new["insertion_time"] / old["insertion_time"]
                )

                insertion_count_ratio = (
                    new["insertion_ops"] / old["insertion_ops"]
                )

                counting_time_ratio = (
                    new["counting_time"] / old["counting_time"]
                )

                counting_count_ratio = (
                    new["counting_ops"] / old["counting_ops"]
                )

                print("\n", old_n, "->", new_n)

                print(
                    "  Insertion time ratio:",
                    round(insertion_time_ratio, 3)
                )

                print(
                    "  Insertion count ratio:",
                    round(insertion_count_ratio, 3)
                )

                print(
                    "  Counting time ratio:",
                    round(counting_time_ratio, 3)
                )

                print(
                    "  Counting count ratio:",
                    round(counting_count_ratio, 3)
                )


def main():
    sizes = [64, 256, 1024, 4096]

    # makes the random data the same each time the program runs
    random.seed(261)

    for n in sizes:
        run_test(n, 8 * n, "8n")
        run_test(n, n ** 2, "n^2")

    print_ratios()


if __name__ == "__main__":
    main()