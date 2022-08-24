SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['大屏展示', '用户管理', '优惠券管理', '车辆管理', '首页管理', '娱乐与购物'],  # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [
        {

            'name': '大屏展示',
            'icon': 'fa fa-desktop',
            'url': '/index/'
        },
        {
            'app': 'user',  # 关联哪个app
            'name': '用户管理',
            'icon': 'fa fa-user',
            'models': [
                {
                    'name': '用户',
                    'icon': 'fa fa-user',
                    'url': 'user/user/'
                },
            ]
        },
        {
            'app': 'coupon',
            'name': '优惠券管理',
            'icon': 'fa fa-gift',
            'models': [
                {
                    'name': '优惠券管理',
                    'icon': 'fa fa-gift',
                    'url': 'coupon/coupon/'
                },
            ]
        },
        {
            'app': 'cars',
            'name': '车辆管理',
            'icon': 'fa fa-car',
            'models': [
                {
                    'name': '车辆',
                    'icon': 'fa fa-taxi',
                    'url': 'cars/car/'
                },
                {
                    'name': '车辆详情',
                    'icon': 'fa fa-car',
                    'url': 'cars/cardetail/'
                },
                {
                    'name': '厂商',
                    'icon': 'fa fa-taxi',
                    'url': 'cars/carfactory/'
                },
                {
                    'name': '车辆展示',
                    'icon': 'fa fa-car',
                    'url': 'cars/carsimg/'
                },
                {
                    'name': '待审核车辆',
                    'icon': 'fa fa-spinner',
                    'url': 'approval/carpendingapproval/'
                },

            ]
        },
        {
            'app': 'home',
            'name': '首页管理',
            'icon': 'fa fa-image',
            'models': [
                {
                    'name': '轮播图',
                    'icon': 'fa fa-th-large',
                    'url': 'home/banner/'
                },
            ]
        },
        {
            # 自2021.02.01+ 支持多级菜单，models 为子菜单名
            'name': '娱乐与购物',
            'icon': 'fa fa-file',
            # 二级菜单
            'models': [
                {
                    'name': '娱乐',
                    'icon': 'far fa-surprise',
                    # 第三级菜单 ，
                    'models': [
                        {
                            'name': '爱奇艺',
                            'url': 'https://www.iqiyi.com/dianshiju/'
                            # 第四级就不支持了，element只支持了3级
                        }, {
                            'name': '百度问答',
                            'icon': 'far fa-surprise',
                            'url': 'https://zhidao.baidu.com/'
                        }
                    ]
                },
                {
                    'name': '购物',
                    'icon': 'far fa-surprise',
                    # 第三级菜单 ，
                    'models': [
                        {
                            'name': '淘宝',
                            'url': 'https://www.taobao.com'
                            # 第四级就不支持了，element只支持了3级
                        }, {
                            'name': '1688',
                            'icon': 'far fa-surprise',
                            'url': 'https://www.1688.com/'
                        }
                    ]
                }

                , ]
        },
    ]
}

# simpleUi隐藏显示服务器信息，快速操作
SIMPLEUI_HOME_INFO = False

# 隐藏快速操作
# SIMPLEUI_HOME_QUICK = False

# 使用分析
SIMPLEUI_ANALYSIS = False

# 隐藏最近动作
SIMPLEUI_HOME_ACTION = False

# 更换网站Logo
SIMPLEUI_LOGO = 'https://ts1.cn.mm.bing.net/th/id/R-C.59e9ef10606e0627f6ab8a911a2f19bd?rik=879%2fISEF%2fLBGfQ&riu=http%3a%2f%2fwww.kuaipng.com%2fUploads%2fpic%2fw%2f2020%2f06-24%2f86414%2fwater_86414_260_260.png&ehk=F%2fwbbHuehMzNz6GdFILpFs3zhFvALmpOehldKU96nt4%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1'
