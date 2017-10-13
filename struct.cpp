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


https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx9aac9c21368447e6&redirect_uri=https%3a%2f%2ftest.xinlianxd.com%2f&response_type=code&scope=snsapi_base#wechat_redirect 


https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf0e81c3bee622d60&redirect_uri=http%3A%2F%2Fnba.bluewebgame.com%2Foauth_response.php&response_type=code&scope=snsapi_userinfo&state=200#wechat_redirect 