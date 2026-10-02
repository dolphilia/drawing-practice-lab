# C：未提示角度 / two-boxes-E2

合成モデル定義と目標カメラから投影を組み立てる仕様。
モデルは人体の正解ではない。

```json
{
  "model": {
    "id": "two-boxes",
    "parts": [
      {
        "id": "L",
        "type": "box",
        "size": [
          1.3,
          0.7,
          0.65
        ],
        "center": [
          0,
          -0.7,
          0
        ],
        "yaw_deg": -15
      },
      {
        "id": "U",
        "type": "box",
        "size": [
          1,
          1,
          0.8
        ],
        "center": [
          0.15,
          0.6,
          0
        ],
        "yaw_deg": 20
      }
    ]
  },
  "camera": {
    "id": "E2",
    "split": "evaluation",
    "azimuth_deg": 155,
    "elevation_deg": 30
  },
  "image": {
    "width": 800,
    "height": 800,
    "scale_px_per_unit": 200,
    "origin_px": [
      400,
      410
    ]
  }
}
```

座標軸・回転と投影の定義は [仕様](../README.md) を参照。解答フォルダは出題中に開かない。
