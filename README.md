# data-collection

## neo4j数据库导入说明

### 1 打开neo4j desktop并新建数据库

### 2 点击新建数据库的manage

### 3 点击open folder，注意此时数据库是关闭的

![image-20200509210759656](https://tva1.sinaimg.cn/large/007S8ZIlly1gemi5ss44zj30y00ista5.jpg)

### 4 在终端打开bin文件夹

![image-20200509210902986](https://tva1.sinaimg.cn/large/007S8ZIlly1gemi6u9utzj31320su4ch.jpg)

### 5 将本项目中import文件夹整体复制到bin文件夹下

![image-20200509210944322](https://tva1.sinaimg.cn/large/007S8ZIlly1gemi7kh8phj31320sudm0.jpg)

### 6 在终端运行命令，导入数据库

```bash
./neo4j-admin import \
    --id-type=STRING \
    --skip-duplicate-nodes=true \
    --ignore-empty-strings=true \
    --nodes=import/company.csv \
    --nodes=import/concept.csv \
    --nodes=import/holder.csv \
    --nodes=import/manager.csv \
    --relationships=import/company_concept.csv \
    --relationships=import/holder_company.csv \
    --relationships=import/manager_company.csv
```

![image-20200509211159015](https://tva1.sinaimg.cn/large/007S8ZIlly1gemi9w4x2ij30ky07c0wb.jpg)

### 7 在neo4j desktop中启动数据库，通过neo4j browser进行浏览

```cypher
match (h :Holder {holderId: "7"}) return h
```

双击节点可以展开

![graph](https://tva1.sinaimg.cn/large/007S8ZIlly1gemieh43dwj30wl0hvk4x.jpg)