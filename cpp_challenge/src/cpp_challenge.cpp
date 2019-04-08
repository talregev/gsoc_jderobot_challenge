#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include <fstream>
#include <algorithm>
#include <tuple>

#define WALL   '#'
#define GROUND '.'

typedef enum {
    Upper,
    Lower,
    Left,
    Right,
} Directions;

/**
 * Find longest path from a cell inside given maze
 * @param maze      - Maze of the problem as matrix
 * @param visited   - Visited matrix. if we visit along the path
 * @param path      - Longest path result
 * @param i         - Row index in the maze
 * @param j         - Column index in the maze
 * @return The length of the longest path from the cell
 */
int find_longest_path(const std::vector<std::vector<char>> &maze, std::vector<std::vector<bool>> visited,
                      std::vector<std::tuple<int, int>> &path, int i, int j);

/**
 * Print matrix. vector of vector
 * @tparam T        - Assuming can print with std::cout
 *                    The inner parameter inside the matrix
 * @param matrix    - The matrix you want to print
 */
template <class T>
void print_matrix(std::vector<std::vector<T>> matrix);

int main() {
    //Read the input
	std::ifstream infile("../mazes/02.txt");
	std::string line;
	std::vector<std::vector<char>> maze;
    while (std::getline(infile, line)) {
        std::vector<char> row(line.begin(), line.end());
        // Can add a check for valid the input
        // Assuming correction of the input
        maze.push_back(row);
    }

    //In case of empty maze
    if (maze.size() == 0 || maze[0].size() == 0) {
        std::cout << "0\n";
        print_matrix(maze);
        exit(0);
    }

    //Data structure for solve the problem
    std::vector<std::vector<bool>> visited(maze.size(), std::vector<bool>(maze[0].size(), false));
    int maze_size = maze.size() * maze[0].size();
    std::vector<std::vector<std::tuple<int,int>>> paths(maze_size);
    std::vector<int> max_vec(maze_size);
    std::vector<int>::iterator max_result;

    // Check the long path from each cell in the maze
    for(int i = 0; i < maze.size(); ++i) {
        for(int j = 0; j < maze[0].size(); ++j) {
            std::vector<std::tuple<int,int>> path;
            int length = find_longest_path(maze, visited, path, i, j);
            int index  = i * maze.size() + j;
            paths[index]   = path;
            max_vec[index] = length;
        }
    }

    // Calculate max length of all paths of each cell
    max_result = std::max_element(max_vec.begin(), max_vec.end());
    int index = std::distance(max_vec.begin(), max_result);
    std::vector<std::tuple<int,int>> path = paths[index];

    // Mark the path inside the maze
    for (int i = 0; i < path.size(); ++i) {
        std::tuple<int,int> tuple = path[i];
        maze[std::get<0>(tuple)][std::get<1>(tuple)] = '0' + i;
    }

    // Print the result
    std::cout << *max_result << "\n";
    print_matrix(maze);


}

int find_longest_path(const std::vector<std::vector<char>> &maze, std::vector<std::vector<bool>> visited,
                      std::vector<std::tuple<int, int>> &path, int i, int j) {

    // Check is valid
    if(i < 0 || i == maze.size() || j < 0 || j == maze[0].size()) {
        return 0;
    }

    // Check if it a wall
    if (maze[i][j] == WALL) {
        return 0;
    }

    // Check if we visit
    if(visited[i][j]) {
        return 0;
    }

    // Mark as visit
    visited[i][j] = true;

    path.push_back(std::make_tuple(i,j));
    std::vector<std::tuple<int,int>> upper_path(path), lower_path(path), left_path(path), right_path(path);

    // Cell directions
    int upper = 1 + find_longest_path(maze, visited, upper_path, i - 1, j);
    int lower = 1 + find_longest_path(maze, visited, lower_path, i + 1, j);
    int left  = 1 + find_longest_path(maze, visited, left_path, i, j - 1);
    int right = 1 + find_longest_path(maze, visited, right_path, i, j + 1);

    std::vector<int> max_vec = {upper, lower, left, right};
    std::vector<int>::iterator max_result;

    max_result = std::max_element(max_vec.begin(), max_vec.end());
    int cell = std::distance(max_vec.begin(), max_result);

    switch (cell) {
        case Upper:
            path = upper_path;
            break;
        case Lower:
            path = lower_path;
            break;
        case Left:
            path = left_path;
            break;
        case Right:
            path = right_path;
            break;
    }

    return *max_result;
}

template <class T>
void print_matrix(std::vector<std::vector<T>> matrix) {
    for (auto& row : matrix) {
        for (auto cell : row) {
            std::cout << cell;
        }
        std::cout << "\n";
    }
}