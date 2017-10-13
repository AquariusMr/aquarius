#include "iostream"
#include "string"

using namespace std;

namespace skt{

    struct Test 
    {
        string name;
        int age;

        Test(string name, int age ){
            this->name = name;
            this->age = age;
        }

        ~Test(){}

        string GetName(){
            return name;
        }

        int GetAge(){
            return age;
        }
    };
}

using namespace skt;


void test (int num){
    cout << num << endl;
}

int main(int argc, char const *argv[])
{
    Test author("shihonggguang", 27);

    void (*p)(int);

    p = test;

    p(1);

    cout << author.GetName() << "\n" << author.GetAge() << endl;
    return 0;
}