#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <math.h>

// int factorial_arr(int fac_arr[20]){
//     // int res_arr[20];
//     fac_arr[0] = 1;
//     for (int i=1; i<20; i++){
//         fac_arr[i] = fac_arr[i-1] * i;
//     }
//     return 0;
// }

// double factorial(int num, int fac_arr[20]){
//     return fac_arr[num];
// }

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
    if (m == 0){
        if (k == 0){
            return 1;
        }
        else if (k == 1){
            return cos(theta);
        }
        else if (k > 1){
            double factor_1 = caculate_pkm(k-1,m,theta) * cos(theta) * (2*k-1);
            double factor_2 = caculate_pkm(k-2,m,theta) * cos(theta) * (k-1);
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
    return caculate_nkm(k,m) * caculate_pkm(k,m,theta);
}



namespace py = pybind11;

PYBIND11_MODULE(legendre,m)
{
  m.doc() = "pybind11 example legendre";

  m.def("normalize", &normalize_pkm, "legendre normalize");
}



// int main(){

//     int fac_arr[20];
//     // factorial_arr(fac_arr);

//     // double a = caculate_nkm(6,2,fac_arr);
//     // double a = caculate_pkm(5,2,0.5);
//     double a = normailize_pkm(4,2,0.55);

//     std::cout << a << std::endl;
// }