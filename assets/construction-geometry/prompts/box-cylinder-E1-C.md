# C：未提示角度 / box-cylinder-E1

合成モデル定義と目標カメラから投影を組み立てる仕様。
モデルは人体の正解ではない。

```json
{
  "model": {
    "id": "box-cylinder",
    "parts": [
      {
        "id": "B",
        "type": "box",
        "size": [
          1.4,
          0.8,
          1
        ],
        "center": [
          0,
          -0.6,
          0
        ],
        "yaw_deg": 0
      },
      {
        "id": "C",
        "type": "cylinder",
        "radius": 0.38,
        "height": 1.3,
        "segments": 24,
        "center": [
          0.2,
          0.45,
          0
        ],
        "yaw_deg": 0
      }
    ]
  },
  "camera": {
    "id": "E1",
    "split": "evaluation",
    "azimuth_deg": 65,
    "elevation_deg": 20
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
