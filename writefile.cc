#include "Aux.h"
int main(void){
    std::string file = "test.txt";
    std::string s = "hallo1";
    std::ofstream f;
    f.open(file,std::ios::app);
    f << s << std::endl;
    f.close();
    f.open(file,std::ios::app);
    f << "hallo2" << std::endl;
    f.close();
    std::vector<double> v {2., 3., 2.5};
    const char X = 'X';
    append_values_to_file(file,v);
    std::string s2 = vec_to_line(v,X);
    std::cout << s2 << std::endl;
    f.open(file,std::ios::app);
    f << s2 << std::endl;
    f.close();
    return 0;
}