//Валя
#include "Aux.h"
#include <unistd.h>
#include <ctime>
#include <filesystem>
#include <iomanip>


#include "ceres/ceres.h"
//#include "glog/logging.h"

using ceres::CENTRAL;
using ceres::CostFunction;
using ceres::NumericDiffCostFunction;
using ceres::Problem;
using ceres::Solve;
using ceres::Solver;

void run_setup(){
    
    /*
    int order_of_uTMD_and_FF = 2;

    std::string runlimitsfile = "archive/rminmax";
    int iRmin, iRmax;
    std::vector<std::string> vf = file_to_vec(runlimitsfile);
    iRmin = stoi(vf[0]);
    iRmax = stoi(vf[1]);
    int iRun = iRmin;
    
    for(int i = iRmin; i <= iRmax; ++i){
        std::string dirname = "archive/run" + std::to_string(i);
        bool t = IsPathExist(dirname);
        std::cout << i << " " << t << std::endl;
        if(t)
            continue;
        
        if(i > iRmax){
            warning("max runs in directory reached.");
            exit(0);
        }
        iRun = i;
        break;
    }
    std::string rundir = "archive/run" + std::to_string(iRun);
    modsys("mkdir " + rundir);
    modsys("cd " + rundir);
    system("ls");
    modsys("mkdir " + rundir + "/com");
    
    //exit(2);
    int version =-1;
    std::cout << "which version of artemide?    ";
    std::cin >> version;
    std::cout << std::endl;
    
    int order;
    std::cout << "which order NXLO?    ";
    std::cin >> order;
    std::cout << std::endl;

    std::string constfile;
    if(order == 0){
        constfile = "constfiles/constfile_N0LO";
        if(version == 0){
            constfile += "_sv19";
        }
    }
    else{
        std::string constfolderadd = "sv19/";
        if(version == 1){
            constfolderadd = "next1/";
        }
        constfile = "constfiles/" + std::to_string(order_of_uTMD_and_FF) + "/constfile_N" + std::to_string(order) + "LO";
    }
    modsys("cp " + constfile + " " + rundir+"/constfile");
    std::cout << " this is run number " << iRun << std::endl;
    */
    //timestamp
    std::time_t result = std::time(nullptr);
    std::ofstream ofs;
    ofs.open("timestamp",std::ios_base::app);
    ofs << "start=" << std::asctime(std::localtime(&result)) << std::endl;
    ofs.close();
    
    //modsys("python milano2.py " + std::to_string(iRun) + " " + std::to_string(order) + " &");
    return;
}

void ping(int l, char mode){
    //std::cout << "create pystop" << std::endl;
    std::string pyblockerfile = "pystopper";
    //std::ofstream ofblock(pyblockerfile);
    //ofblock.close();
    modsys("touch pystopper");
    std::string file;
    if(mode == 'p')
        file = "com/milano.py.ctrl";
    else if(mode == 'c')
        file = "com/milano.cc.ctrl";
    else {std::cout << "undefined command: " << mode << std::endl; exit(2);}
    std::ofstream f;
    f.open(file);
    f << l;
    f.close();
    char name_char [pyblockerfile.size()];
    for(unsigned int i = 0; i < pyblockerfile.size(); ++i){
        name_char[i] = pyblockerfile[i];
    }
        
    //int status = std::remove(name_char);
    //std::remove(pyblockerfile);
    //system("rm pystopper -f");
    modsys("rm pystopper -f");
    //std::cout << status << " ping result..." << std::endl;

    //if(!status)
    //    std::cout << "remove did not work" << std::endl;
    //std::filesystem::remove(pyblockerfile); //did not work at hpd..
    //std::cout << "pystop should be over..." << std::endl;
    return;
}


void run_finalize(){
    ///timestamp
    std::time_t result = std::time(nullptr);
    std::ofstream ofs;
    ofs.open("timestamp");
    ofs << "end=  " << std::asctime(std::localtime(&result)) << std::endl;
    ofs.close();
    ping(0,'p');
    //system("touch finished correctly") //one can also check for timestamp.
}

void checkControlFile(bool& run){
    std::string cppblockerfile = "cppstopper";
    bool gate1 = check_File_exists(cppblockerfile);

    while(gate1){
        usleep(200000);
        gate1 = check_File_exists(cppblockerfile);
    }
    std::string adress = "com/milano.cc.ctrl";
    std::ifstream f(adress);
    checkIFile(f,adress);
    std::string s;
    getline(f,s);
    int cmd = stoi(s);
    switch(cmd){
        case 0:
            std::cout << "end program called by command" << std::endl;
            exit(0);
            break;
        case 1://go on
            run = true;
            break;
        case 2://wait
            run = false;
            break;
        default:
            std::cout << "unknown control command:" << std::endl << cmd << std::endl;
            exit(2);
    }   
    return;
}

void readParameters(std::string file, std::vector<double> &dv, unsigned int line){
    std::ifstream f;
    f.open(file);
    checkIFile(f,file);
    std::string s;
    getline(f,s,line);
    const char space = ' ';
    std::vector<std::string> vs = line_to_vec(s,space);
    for(unsigned int i = 0; i < vs.size(); ++i){
        dv[i] = stod(vs[i]);
    }

    f.close();
}

void wait4go(bool& run){
    do
    {
    int local_timer = 30000;
    usleep(local_timer);
    checkControlFile(run);
    } while (!run); //as long run is false we wait..
    return; //once loop is broken we can go on.
}

//double functioncall(double x1, double x2){
double functioncall(const double * x){

    //atm: hard code parameters here
    std::vector<double> parameters {2.0, 0.039, 0.184739, 6.22437, 588.193, 2.44327,-2.51106, 0.0, 0.0,0.3906, 0.4388, 0.4261, 0.4799};
    //std::cout << " functioncall with x1 = " << x[0] << " x2 = " << x[1] << std::endl;
    //std::cout << " functioncall with x1 = " << x1 << " x2 = " << x2 << std::endl;
    //adapt..
    double x1 = x[0];
    //double x2 = x[1];

    parameters[1] = x[0];
    for(unsigned int i = 1; i < 6;++i){
        parameters[i+1] = x[i];
    }
    for(unsigned int i = 6; i < 9;++i){
        parameters[i+3] = x[i];
    }
    
    //parameters[1] = x1; // for testing
    //parameters[2] = x2;
    std::cout << parameters << std::endl;
    /*unsigned int npmod = 1; // number of np parameters that we modify here..
    for(unsigned int i = 0; i < npmod; ++i){
        if(i < 6)
            parameters[i+1] = x[i]; //TMD paras
        else if ( i >= 6)
            parameters[i+3] = x[i]; //FF params
    }
    */
    const char spacebar = ' ';
    

    //write parameters
    std::ofstream ofs;
    std::string adress = "com/milano.cc.parameters";
    ofs.open(adress);
    checkOFile(ofs,adress);
    std::string s = vec_to_line_precision(parameters, spacebar, 50);
    ofs << std::fixed << std::setprecision(50) << s;
    ofs.close();
    std::cout << "\033[1;37m";
    std::cout << "c++ calls for value from python with parameters " << s << std::endl;
    std::cout << "\033[0m";
    for(unsigned int i = 0; i < 10; ++i){
        std::cout << x[i] << " ";
    }
    std::cout << std::endl;
    /*  
    double *pointer_parameters = (double*) malloc (parameters.size());
    for(unsigned int k = 0; k < parameters.size(); ++k){
        pointer_parameters[k] = parameters[k];
    }
    std::cout << pointer_parameters << " " << pointer_parameters[3] << std::endl;
    */
    
    //system("cat com/milano.cc.parameters");
    //std::cout << "call python with parameters: " << parameters << std::endl;


    ping(2,'c');
    ping(1,'p');
    bool run_local = false; 
    wait4go(run_local);
    //now python is called and c knows that is has to wait until python wakes it up.
    //after wake up:
    //free(pointer_parameters);
    std::ifstream ifs;
    std::string py_result_file = "com/milano.py.result";
    ifs.open(py_result_file);
    getline(ifs,s);
    ifs.close();
    //remove the file such that you cannot read it again by accident.
    modsys("rm " + py_result_file + " -f");
    std::cout << "\033[1;35m";
    std::cout << "c++ received value from python " << s << std::endl;
    std::cout << "\033[0m";
    double v = stod(s);
    std::vector<double> saveme = parameters;
    saveme.push_back(v);
    std::string save_vals_file = "valuesgrid";
    append_values_to_file(save_vals_file,saveme);
    //v = sqrt(v);//because ceres later squares this anyway..
    return v;
    //return x1 * x1 ;
}

// Функтор Вальи
/*
struct CostFunctor {
  bool operator()(const double* const x, double* residual) const {
    //std::cout << " CostFunctor with x = " << x[0] << " y = " << x[1] << std::endl;
    //residual[0] = sqrt(functioncall(x[0],x[1])); // function is implemented in python...
    residual[0] = sqrt(functioncall(x)); // function is implemented in python...
    return true;
  }
};*/


struct Rosenbrock {
    bool operator()(const double* parameters, double* cost) const {
    const double x1 = parameters[0];
    const double x2 = parameters[1];
    //std::cout << std::setprecision(50) << " x1 = " << x1 << " x2 = " << x2 << std::endl;
    //cost[0] = (1.0 - x) * (1.0 - x) + 100.0 * (y - x * x) * (y - x * x);
    //cost[0] = functioncall(x,y);
    cost[0] = functioncall(parameters);
    std::cout << "Rosenbrock has received value: " << std::setprecision(50) << cost[0] << std::endl;
    const double relative_step_size = 1e-2;
    //cost[0] = (x+3)*(x+3) + (y-1)*(y-1);
    return true;
  }

  static ceres::FirstOrderFunction* Create() {
    constexpr int kNumParameters = 10;
    //constexpr int kNumParameters = 2;
    //constexpr int kNumParameters = 1;
    return new ceres::NumericDiffFirstOrderFunction<Rosenbrock,
                                                    ceres::CENTRAL,
                                                    kNumParameters>(
        new Rosenbrock);
  }
};


//this is very bad style:
//std::vector<double> initial_values;



int main(int argc, char** argv) {
    
    std::cout << "c++ starting" << std::endl;
    run_setup();
    //exit(1);

    
    ping(2,'p'); // hold python on wait
    
    bool run = true;
    
    for(unsigned int i = 0; i < 0; ++i){

        double x = 0.2*double(i);
        double y = x*x;
        
        //double value = functioncall(x,y);
        //double value = functioncall(x);
        //std::cout << "done with value " << value << std::endl; //alte version
    }
    
    std::cout << "HALLO" << std::endl;
    //google::InitGoogleLogging(argv[0]);
    std::cout << "HALLO" << std::endl;
    // The variable to solve for with its initial value. It will be
    // mutated in place by the solver.
    double x = 0.184739;
    double y = 6.22437;
    const double initial_x = x;
    const double initial_y = y;
    //double z[2] = {x, y};
    //double z[1] = {0.184739};
    //double z[3] = {0.039487913636830296, 0.184739, 6.22437};
    //double z[10] = {0.039487913636830296, 0.184739, 6.22437, 588.193, 2.44327,-2.51106, 0.39066964680746497, 0.43884593436935954, 0.42616597768139564, 0.4799926928570539};
    double z[10] = {0.055053, 0.024426, 6.206236, 588.192860, 2.394060, -2.551509, 0.239846, 0.312764, 0.286254, 0.479993};
    //double z[2] = {0.039487, 0.1847};

    std::vector<int> const_parameters{0,7,8};

    
    std::cout << "  test milano2    " << std::endl;
    std::cout << "milano output for z is : " << functioncall(z) << std::endl;
    ceres::GradientProblemSolver::Options options;
    options.minimizer_progress_to_stdout = true;
    options.function_tolerance  = 0. ;
    options.gradient_tolerance  = 0.;
    options.parameter_tolerance = 0.;
    ceres::GradientProblemSolver::Summary summary;
    ceres::GradientProblem problem(Rosenbrock::Create());


    /*if( const_parameters.size() > 0 ){

                ceres::SubsetManifold *pcssp = new ceres::SubsetManifold( 9, const_parameters );

        problem.parameterization( z, pcssp);
    }*/

    ceres::Solve(options, problem, z, &summary);
    std::cout << summary.FullReport() << "\n";
    //std::cout << "Initial x: " << initial_x << " y: " << initial_y << "\n";
    //std::cout << "Final   x: " << z[0] << " y: " << z[1];
    /*
    // Build the problem.
    Problem problem;

  // Set up the only cost function (also known as residual). This uses
  // numeric differentiation to obtain the derivative (jacobian).
  CostFunction* cost_function =
      new NumericDiffCostFunction<CostFunctor, CENTRAL, 1, 2>(new CostFunctor);
      //new NumericDiffCostFunction<CostFunctor, CENTRAL, 1, 1>(new CostFunctor);
  problem.AddResidualBlock(cost_function, nullptr, &z[0]);

  // Run the solver!
  //options..
  Solver::Options options;
  options.minimizer_progress_to_stdout = true;
  // Set all tolerances to zero to ensure that all fits get to the
  // maximum number of iterations without stopping.
  options.function_tolerance  = 0. ;
  options.gradient_tolerance  = 0.;
  options.parameter_tolerance = 0.;
  //problem.SetParameterLowerBound(&x, 0,     );
  problem.SetParameterLowerBound(z, 1, -10.);
  problem.SetParameterUpperBound(z, 1, 10.);

  options.update_state_every_iteration = true;
  Solver::Summary summary;
  Solve(options, &problem, &summary);

  std::cout << summary.BriefReport() << "\n";
  std::cout << "x : " << initial_x << " -> " << z[0] << "\n";
  std::cout << "y : " << initial_y << " -> " << z[1] << "\n";

    //ping(0,'p'); // end python
    std::cout << "here..." << std::endl;
    ping(2,'p'); // keep python alive



    //if the block below does not work anyway.. it can be removed..
    std::string pyblockerfile = "pystopper";
    char name_char [pyblockerfile.size()];
    for(unsigned int i = 0; i < pyblockerfile.size(); ++i){
        name_char[i] = pyblockerfile[i];
    }
        
    int status = std::remove(name_char);
    */
    run_finalize();
    //
    return 0;
}