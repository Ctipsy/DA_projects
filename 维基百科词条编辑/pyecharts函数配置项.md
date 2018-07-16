## 图形初始化

例如：bar= Bar("正标题", "副标题")

图形大小（width ,height ）,正标题、副标题,支持\n换行,标题位置、标题文字的大小、标题的颜色、画布背景颜色、渲染方式

图形的位置如何设置呢？

## 通用配置项都在add()中进行配置

例如：
``` python
bar.add("statistics", stat_attr, stat_v , mark_point=['max', 'min'],mark_line=["average"],is_label_show =True,
        label_pos ='inside',label_formatter='{c}',xaxis_interval =0,is_datazoom_show =True,legend_pos ='right',legend_top ='center',is_more_utils  =True)
xyAxis：直角坐标系中的 x、y 轴(Line、Bar、Scatter、EffectScatter、Kline)
dataZoom：dataZoom 组件 用于区域缩放，从而能自由关注细节的数据信息，或者概览数据整体，或者去除离群点的影响。(Line、Bar、Scatter、EffectScatter、Kline、Boxplot)
legend：图例组件。图例组件展现了不同系列的标记(symbol)，颜色和名字。可以通过点击图例控制哪些系列不显示。
label：图形上的文本标签，可用于说明图形的一些数据信息，比如值，名称等。
lineStyle：带线图形的线的风格选项(Line、Polar、Radar、Graph、Parallel)
grid3D：3D笛卡尔坐标系组配置项，适用于 3D 图形。（Bar3D, Line3D, Scatter3D)
axis3D：3D 笛卡尔坐标系 X，Y，Z 轴配置项，适用于 3D 图形。（Bar3D, Line3D, Scatter3D)
visualMap：是视觉映射组件，用于进行『视觉编码』，也就是将数据映射到视觉元素（视觉通道）
markLine&markPoint：图形标记组件，用于标记指定的特殊数据，有标记线和标记点两种。（Bar、Line、Kline）
tooltip：提示框组件，用于移动或点击鼠标时弹出数据内容
toolbox：右侧实用工具箱
```

### xyAxis: 坐标轴配置

坐标轴名称、数据标签、坐标轴

数据项

stat_attr, stat_v
坐标轴名称，名称的大小、颜色、位置

x,y轴交换

坐标轴刻度线和标签是否对齐

坐标轴数据反向

是否显示坐标轴

坐标轴刻度标签的显示间隔，0强制全部显示，1隔一个显示，以此类推

标签与坐标轴的距离

坐标轴刻度的最大、小值，不设置默认为自适应

坐标轴标签的字体大小、颜色、旋转角度

y 轴标签格式器，如给标签数据都加上单位

### dataZoom 区域缩放

是否使用区域缩放

缩放类型，inside比较好用

缩放方向

### legend 图例组件

例子中的

statistics
是否显示图例组件

图例的文字大小，颜色，位置，朝向

### label图形上的文本标签，值，名称等

是否正常显示文本标签

标签的位置、大小、颜色

显示名称或者值或者系列名等，模板变量有 {a}, {b}，{c}，{d}，{e}，分别表示系列名，数据名，数据值等

### lineStyle，带线图形的风格

线的宽度、透明度、颜色、类型、是否弯曲

### visualMap 视觉映射组件

根据颜色或者数值大小来控制数据的显示，相当于筛选数据空间，选择查看不同数值的数据

组件文本不显示

通过数值大小来控制失效，通过颜色的可以

加上参数

visual_text_color='#000'即可
是否显示视觉组件

映射方式：通过颜色，或者数值大小来控制数据显示

组件允许的最大最小值

连续型显示

分段性显示

### markLine&markPoint 标记线 标记点

标记最大最小值，标记平均值的线

标记的形状、颜色 、大小

自定义标记的点

标记线可以是任何两点连线

### tooltip

提示框

什么时候触发提示

提示的样式

### toolbox 实用工具箱

是否开启实用工具箱

是否使用更多的实用工具