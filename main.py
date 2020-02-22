import math

def read_file():
    filename = 'input_files/input.txt'

    with open(filename, 'r') as f:
        line1 = f.readline()
        B, L, D = map(int, line1.split())

        book_scores = f.readline().split()

        N = [None] * L
        T = [None] * L
        M = [None] * L

        lib_books = [None] * L

        for lib_i in range(L):
            N[lib_i], T[lib_i], M[lib_i] = map(int, f.readline().split())
            lib_books[lib_i] = sorted([(id, book_scores[id]) for id in map(int, f.readline().split())], key=lambda x: x[1], reverse=True)

        return B, L, D, N, T, M, lib_books


def write_file(output):
    filename = 'output.txt'
    with open(filename, 'w') as f:
        for line in output:
            f.write(str(line) + '\n')

def reward_in_remaining_days(sent_books, books_in_lib, days_left, M, T, lib_id):
    global current_best_books
    no_of_books_we_can_send = days_left*M
    remaining_books = set(books_in_lib) - sent_books
    remaining_books = list(remaining_books)
    remaining_books = sorted(remaining_books, key=lambda x: x[1], reverse=True)
    remaining_books = remaining_books[:(no_of_books_we_can_send+1)]
    current_best_books[lib_id] = remaining_books
    total_reward = sum([int(book[1]) for book in remaining_books]) / math.sqrt(T)
    return total_reward

def algorithm(B, L, D, N, T, M, lib_book_ids):
    global books_we_send_now
    not_signed_up_libs = set(range(L))
    sent_books = set()
    days_left = D + 1
    total_score = 0

    output = []

    while days_left > 0 and len(not_signed_up_libs) > 0:
        lib_rewards = [reward_in_remaining_days(sent_books, lib_book_ids[lib_id], days_left, M[lib_id], T[lib_id], lib_id) if lib_id in not_signed_up_libs else -10**100 for lib_id in range(L)]
        best_lib = lib_rewards.index(max(lib_rewards))

        not_signed_up_libs.remove(best_lib)
        days_left -= T[best_lib]

        print(days_left)

        send_now = current_best_books[best_lib]
        sent_books.update(send_now)

        send_now_ids = [str(book[0]) for book in send_now]

        output.append(f"{best_lib} {len(send_now)}")
        output.append(' '.join(send_now_ids))

    output.insert(0, int(len(output)/2))
    write_file(output)

if __name__ == "__main__":
    B, L, D, N, T, M, lib_book_ids = read_file()
    current_best_books = [None] * L
    algorithm(B, L, D, N, T, M, lib_book_ids)
