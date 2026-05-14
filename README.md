# acsl_package

ハードウェア固有ドライバ（ブランチ単位で管理）

## ublox (RTK-GNSS)

u-blox RTK-GNSS レシーバ用 ROS2 ドライバ。

### ビルド

```bash
dbuild <base_image> ublox ublox
```

### 起動

```bash
dup ublox
```

### 設定

環境変数:
- `UBLOX_DEVICE`: デバイスパス (default: `/dev/ttyACM0`)
- `UBLOX_BAUDRATE`: ボーレート (default: `115200`)

udev ルール: `rules/ublox.rules`

### 公開トピック

- `/fix` (sensor_msgs/NavSatFix) — 緯度・経度・高度
- `/navpvt` (ublox_msgs/NavPVT) — PVT (Position, Velocity, Time)
