#from matrix import create_matrix, get_value, set_value
from matrix import input_matrix

def main():
    print("3×3 배열을 입력하세요.")

    matrix = input_matrix()

    print("\n입력한 배열:")
    for row in matrix:
        print(row)


if __name__ == "__main__":
    main()