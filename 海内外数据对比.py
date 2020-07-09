from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
import get_save
from pyecharts.charts import Pie
from pyecharts import options as opts

name_dict = get_save.name_dict

# 1.获取数据
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=318749413808"
data_json = get_save.url_to_data(url)
world_data = data_json["data"]["areaTree"]

china_today_data = data_json["data"]["chinaTotal"]["total"]
china_today_time = data_json["data"]["lastUpdateTime"]

world_data = get_save.get_data(world_data, ["id", "name", "lastUpdateTime"])
world_data.rename(columns=name_dict, inplace=True)

world_data.set_index('名称', inplace=True)

world_data['当日现存确诊'] = world_data['累计确诊'] - world_data['累计死亡'] - world_data['累计治愈']
china_data_store_confirm = int(world_data['当日现存确诊'].loc['中国'])

world_data = world_data.drop('中国', axis=0)
world_data_store_confirm = int(world_data['当日现存确诊'].sum())
world_confirm = int(world_data['累计确诊'].sum())
world_heal = int(world_data['累计治愈'].sum())
world_dead = int(world_data['累计死亡'].sum())

oversea_data = {
    "confirm": [['国内', int(china_today_data['confirm'])], ['国外', world_confirm]],
    "heal": [['国内', int(china_today_data['heal'])], ['国外', world_heal]],
    "dead": [['国内', int(china_today_data['dead'])], ['国外', world_dead]],
    "store_confirm": [['国内', china_data_store_confirm], ['国外', world_confirm]]

}
subtitle = " 更新时间：" + china_today_time


fn = """
    function(params) {
        if(params.name == '国外')
            return '\\n\\n\\n' + params.name + ' : ' + params.value;
        return params.seriesName + '\\n' + params.name + ' : ' + params.value;
    }
    """


def new_label_opts():
    return opts.LabelOpts(formatter=JsCode(fn), position='center')


pie = (Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
    .add('现存确诊',
         oversea_data['store_confirm'],
         center=['30%', '25%'],
         radius=[60, 90],
         label_opts=new_label_opts()
         )
    .add('累计确诊',
         oversea_data['confirm'],
         center=['30%', '75%'],
         radius=[60, 90],
         label_opts=new_label_opts()
         )
    .add('累计治愈',
         oversea_data['heal'],
         center=['75%', '25%'],
         radius=[60, 90],
         label_opts=new_label_opts()
         )
    .add('累计死亡',
         oversea_data['dead'],
         center=['75%', '75%'],
         radius=[60, 90],
         label_opts=new_label_opts()
         )
    .set_global_opts(
         title_opts=opts.TitleOpts(title="海内外疫情数据对比",
                              subtitle=subtitle),
         legend_opts=opts.LegendOpts(is_show=True), )
    .set_series_opts(
         tooltip_opts=opts.TooltipOpts(
         trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"), )

)
pie.render('海内外数据对比.html')
