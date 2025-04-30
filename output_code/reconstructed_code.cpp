
#include <iostream>
#include <vector>
#include <stdexcept>
#include <numeric>

class Student {
public:
    Student(const std::string& name) : name(name) {}

    void addGrade(int grade) {
        if (grade < 0 || grade > 20) {
            throw std::invalid_argument("Grade must be between 0 and 20.");
        }
        grades.push_back(grade);
    }

    double average() const {
        if (grades.empty()) {
            return 0.0;
        }
        double sum = std::accumulate(grades.begin(), grades.end(), 0);
        return sum / grades.size();
    }

    bool hasPassed() const {
        return !grades.empty() && average() >= 10.0;
    }

private:
    std::string name;
    std::vector<int> grades;
};

int main() {
    // Exemple d'utilisation
    try {
        Student student("Alice");
        student.addGrade(15);
        std::cout << "Average: " << student.average() << std::endl;
        std::cout << "Has passed: " << (student.hasPassed() ? "Yes" : "No") << std::endl;

        student.addGrade(25); // This will throw an exception
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
