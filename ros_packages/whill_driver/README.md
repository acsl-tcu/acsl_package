# whill_driver
WHILL model CRを制御するためのプログラムを管理しているパッケージ
## 実行コマンドの一覧
```
# WHILL CRノードの起動
ros2 run whill_driver whill
```

---
## Subscribe Topics

### `~/cmd_vel` ([geometry_msgs/Twist.msg](http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/Twist.html))
WHILLに送信する速度・角速度指令値
* Vector3  linear
	* float64 x : 速度指令 ($ \mathbb{R^{\pm}} $) [m/s]
	* float64 y : None
	* float64 z : None
* Vector3  angular
	* float64 x : None
	* float64 y : None
	* float64 z : 角速度指令 ($ \mathbb{R^{\pm}} $) [rad/s]
### `~/cmd_power` ([std_msgs/Bool.msg](http://docs.ros.org/en/noetic/api/std_msgs/html/msg/Bool.html))
WHILL model CR の電源制御指令
* bool data : 1 (ON), 0 (OFF)
---
## Parulish Topics
### `~/battery_level` ([std_msgs/Int16.msg](http://docs.ros.org/en/noetic/api/std_msgs/html/msg/Int16.html))
*  int16 data : バッテリー残量 [%]

### `~/battery_current` ([std_msgs/Float64.msg](https://docs.ros.org/en/noetic/api/std_msgs/html/msg/Float64.html))
* float64 data : 給電電流 [mA]
### `~/motor_angle` ([geometry_msgs/Vector3.msg](https://docs.ros2.org/latest/api/geometry_msgs/msg/Vector3.html))
* float64 x : 右ホイール角度($ \pm\pi $) [rad]
* float64 y : 左ホイール角度($ \pm\pi $) [rad]
* float64 z : None
### `~/motor_speed` ([geometry_msgs/Vector3.msg](https://docs.ros2.org/latest/api/geometry_msgs/msg/Vector3.html))
* float64 x : 右ホイール速度 [m/s]
* float64 y : 左ホイール速度 [m/s]
* float64 z : None
### `~/speed_mode` ([std_msgs/Int16.msg](http://docs.ros.org/en/noetic/api/std_msgs/html/msg/Int16.html))
*  int16 data : スピードモード
	|data| Mode |
	|:--:|:--|
	| 0 | Shift 1 |
	| 1 | Shift 2 |
	| 2 | Shift 3 |
	| 3 | Shift 4 |
	| 4 | 外部入力 |
	| 5 | スマホ入力 |

### `~/joy` ([geometry_msgs/Vector3.msg](https://docs.ros2.org/latest/api/geometry_msgs/msg/Vector3.html))
* float64 x : 縦スティック信号 [$\pm$%]
* float64 y : 横スティック信号 [$\pm$%]
* float64 z : None

---
## 参考
https://github.com/WHILL/pywhill
https://github.com/WHILL/whill_control_system_protocol_specification