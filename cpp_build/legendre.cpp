#include <iostream>
#include <limits>
#include <math.h>

using namespace std;

int factorial(int num){
    int res = 1;
    for (int i=1;i<=num;i++){
        res *= i;
    }
    return res;
}

double caculate_nkm(int k,int m){
    double nkm;
    double delta_0m;

    if (m == 0) delta_0m = 1; else delta_0m = 0;
    nkm = (2-delta_0m) * (2*k+1) * factorial(k-m) / factorial(k+m);

    return sqrt(nkm);
}

double caculate_pkm(int k, int m, double theta){
    typedef std::numeric_limits< double > dbl;
    cout.precision(dbl::max_digits10);
    if (m == 0){
        if (k == 0){
            return 1.0;
        }
        else if (k == 1){
            return cos(theta);
        }
        else if (k > 1){
            double factor_1 = caculate_pkm(k-1,m,theta) * cos(theta) * (2*k-1);
            // cout << "factor_1 : " << fixed << k << " " << m << " " << factor_1 << endl;
            // cout << "cos : " << fixed << k << " " << m << " " << cos(theta) << endl;
            double factor_2 = caculate_pkm(k-2,m,theta) * (k-1);
            return (factor_1 - factor_2) / k;
        }
    }
    else if (m >= 1){
        double factor_1 = caculate_pkm(k-1,m-1,theta) * (k+m-1);
        double factor_2 = caculate_pkm(k,m-1,theta) * cos(theta) * (k-m+1);
        double factor_3 = sqrt(1-pow(cos(theta),2));
        return (factor_1-factor_2) / factor_3;
    }
    return 0;
}

double normalize_pkm(int k, int m, double theta){
    // double res_1 = caculate_nkm(k,m);
    // double res_2 = caculate_pkm(k,m,theta);
    // double res = res_1 * res_2;
    return caculate_nkm(k,m) * caculate_pkm(k,m,theta);
}


#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

PYBIND11_MODULE(legendre,m)
{
  m.doc() = "pybind11 example legendre";

  m.def("normalize", &normalize_pkm, "legendre normalize");
}



// int main(){

//     double a = normalize_pkm(4,2,0.555555);
//     // std::cout << a << std::endl;

// }