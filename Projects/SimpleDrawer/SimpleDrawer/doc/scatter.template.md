# 散点图的模板说明
| 参数         | 类型                            | 作用                                             |
|------------|-------------------------------|------------------------------------------------|
| title      | str                           | 图幅名字                                           |
| theme      | int                           | 图幅主题，从0~7分别对应亮色、天蓝色、暗色、棕色、NCS蓝色、高对比度、冰蓝色主题Qt主题 |
| polar      | bool                          | true的时候是极坐标图，反之是直角坐标系图                         |
| shape      | str/list[str]                 | 散点形状，c表示对应位置图点状为圆形，r表示方形                       |
| size       | float/list[float]             | 散点大小                                           |
| color      | str/list[str]                 | 图颜色                                            |
| categories | str/list[str]                 | 图类名字                                           |
| xs         | list[float]/list[list[float]] | x坐标集合                                          |
| ys         | list[float]/list[list[float]] | y坐标集合                                          |
| xrange     | list[int] and len == 2        | x轴显示范围                                         |
| yrange     | list[int] and len == 2        | y轴显示范围                                         |
| xlabel     | str                           | x轴标签                                           |
| ylabel     | str                           | y轴标签                                           |


## 模板案例
```json
{
  "title" : "散点图名字",
  "theme" : 2,
  "polar" : false,
  "shape" : ["c", "r", "r"],
  "size" : [20, 20, 30],
  "color" : ["red", "blue", "grey"],
  "categories" : ["A Type", "B Type", "C Type"],
  "xs" : [
    [1, 2, 3, 4],
    [0.5, 0.7, 1.2, 4],
    [0.5, 0.7, 1.2, 4]
  ],
  "ys" : [
    [3, 4, 5, 6],
    [1, 3, 7, 3],
    [0, 3, 2, 6]
  ],
  "xrange" : [-5, 10],
  "yrange" : [-2, 10],
  "xlabel" : "标签1",
  "ylabel" : "标签2"
}```