#include <stdio.h>

int employee_count = 10;
float company_revenue = 20.5;
double company_expenses = 30.7;
char department_code = 'A';
long total_assets = 100000;

int employeeCount = 10;
float companyRevenue = 20.5;
double companyExpenses = 30.7;
char departmentCode = 'A';
long totalAssets = 100000;

typedef struct {
    int number_of_employees;
    float revenue_in_millions;
} company_info;

typedef struct {
    char company_name[100];
    int year_established;
} company_details;

typedef struct {
    int numberOfEmployees;
    float revenueInMillions;
} companyInfo;

typedef struct {
    char companyName[100];
    int yearEstablished;
} companyDetails;

void print_employee_info();
int calculate_total_revenue();
float calculate_average_salary();

void printEmployeeInfo();
int calculateTotalRevenue();
float calculateAverageSalary();

#define MAX_EMPLOYEES 100
#define MIN_SALARY 30000

#define max_employees 100
#define min_salary 30000
#define average_salary 50000

enum companyStatus {STARTUP, GROWING, ESTABLISHED};


enum CompanySize {SMALL, MEDIUM, LARGE};
enum EmployeeRole {CEO, MANAGER, ENGINEER};

int main() {
    company_info myCompany = {50, 500000.5};
    company_details myDetails = {"TechCorp", 2005};

    printf("Company Name: %s\n", myDetails.company_name);
    printf("Company Revenue: %.2f\n", myCompany.revenue_in_millions);

    for(int i = 0; i<10;i++){
        printf("Hello World!");
    }

    return 0;
}
