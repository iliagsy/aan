# include <cstdio>
# include <cmath>
using namespace std;

# define nCoord 50000  // number of data rows
# define MPC 0.003846154  // meter per count
# define Pi 3.1415926

class Data {
	double theta;
	double x, y;
	Data(old_theta) {
		theta = old_theta;
	}
	Data(){};
};


class Alg {
private:
	double old_theta;
public:
	Alg() {
		old_theta = -137.875 / 180 * Pi;
	}
	double calc_delta_trans(int pulse1, int pulse2) {
		/*
			返回：单位：米
		*/
		if(pulse2 < pulse1)
			pulse2 += 30000;
		return MPC * (pulse2 - pulse1);
	}
	double calc_delta_rot(double yaw1, double yaw2) {
		/*
			传入：单位：角度
			返回：角度
		*/
		return yaw2 ／ 180 * Pi - yaw1 / 180 * Pi;
	}
	Data calc_next_coords(double x, double y, double delta_trans, \
												double delta_rot, double theta) {
		Data res(theta);
		theta_hat = theta + delta_rot / 2;
		res.x = x + cos(theta_hat) * delta_trans;
		res.y = y + sin(theta_hat) * delta_trans;
		return res;
	}
	void update_theta(theta) {
		old_theta = theta;
	}
};
