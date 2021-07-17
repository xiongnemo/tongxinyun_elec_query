# tongxinyun_elec_query
Gets the amount of electricity remaining for dorms registered in your Tongjixun account.

## 使用的先决条件

能从 Android 平台上的 `同心云` 客户端中提取出其数据文件夹下的 `shared_prefs/EMP_SHELL_SP_KEY.xml` 文件，或者从同心云的流量中找到 `openToken`。

## 环境

`Python 3`

## 依赖

```bash
pip3 install requests
```

## 使用

可以单独使用，也可以在别的文件中使用。

### 单独使用

```bash
python3 ./tongxinyun_elec_query.py -o <openToken>
```

或者

```bash
python3 ./tongxinyun_elec_query.py --openToken=<openToken>
```

它会在终端上打印出每条记录对应的宿舍楼，房间和剩余电量。

### 在别的文件中使用

```python3
from tongxinyun_elec_query import tongxinyun_elec_query

tongxinyun_open_token = "***"

print(tongxinyun_elec_query(tongxinyun_open_token))
```

`tongxinyun_elec_query` 直接返回从同心云校园钱包获得的如下信息：

```json
{'code': 0,
 'data': [{'area': '******',
           'areaName': '******',
           'building': '******',
           'buildingId': '******',
           'dataDt': ******,
           'isDefault': '******',
           'remain': **.**,
           'room': '******',
           'roomId': '******',
           'userId': '******',}],
           ...,
 'msg': 'success'}
```
