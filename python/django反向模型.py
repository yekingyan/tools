import re
import os

class CreateModel:

    def __init__(self, table_desc, model_text):
        self.table_desc = table_desc
        self.model_text = model_text

    def parse_text(self):
        """
        解析文本
        :return: list -> [field_i, field_name, field_type, field_max_len, field_desc]
        """
        table_desc = self.table_desc
        item_list = table_desc.split('\n')
        fields_list = [item.split('\t') for item in item_list if '\t' in item]
        return fields_list

    def help_text_to_field(self):
        """
        生成字段对段的help_text
        :return: dict -> filed: help_text
        """
        field_array = self.parse_text()
        d = {}
        for i in field_array:
            [field_i, field_name, field_type, field_max_len, field_desc] = i
            d[field_name] = field_desc
            d[field_name.lower()] = field_desc
        return d

    def beatify_model(self, lower_case=False):
        """
        field 字段用数据库对应的,
        取db_column的值，删db的值
        :param lower_case: 生成字段是否转成小写字母
        :return:
        """
        strings = self.model_text
        ls = [i for i in strings.split('\n') if i and not re.match(r'^\s*?$', i)]
        re_db_column = re.compile(r"\s*(\w+)\s=\smodels.*?(db_column=\'(\w+)\',*\s*)")
        beatify_ls = []
        for i in ls:
            (db_filed, db_column_parent, db_column) = re_db_column.search(i).groups()
            if not lower_case:
                i = i.replace(db_filed, db_column)
                i = i.replace(db_column_parent, '')
            # 删注释
            i = re.sub(r"\s*?#\s.*?\.", '', i)
            beatify_ls.append(i)
        return '\n'.join(beatify_ls)

    def add_help_text(self, model_text):
        """
        加入help_text 参数
        """
        strings = model_text
        d = self.help_text_to_field()
        ls = [i for i in strings.split('\n') if i]
        re_filed = re.compile(r"\s*(\w+)\s=")
        re_has_params = re.compile(r"\((.*?)\)")
        beatify_ls = []
        for i in ls:
            filed = re_filed.search(i).group(1)
            has_params = re_has_params.search(i).group(1)
            help_text = d.get(filed, 'fuck')
            if has_params:
                i = i.replace("(", f"(help_text='{help_text}', ")
            else:
                i = i.replace("(", f"(help_text='{help_text}'")
            beatify_ls.append(i)
        return '\n'.join(beatify_ls)
    
    def holy_cow(self, lower_case=False):
        string = self.add_help_text(self.beatify_model(lower_case))
        return string


if __name__ == '__main__':

    # table 结构
    table_ds = """
    1	Order_Id	bigint	8	积分订单头部
    2	Order_No	varchar	8000	订单编号
    3	Order_GUID	uniqueidentifier	16	订单GUID
    4	Buyer_User_Id	bigint	8	购买者Id
    5	Buyer_Enterprise_Id	bigint	8	购买者企业Id
    6	Transaction_Integral	bigint	8	交易积分
    7	Earnest_Integral	bigint	8	实际扣除积分
    8	Deduction_Type	int	4	积分扣除的方式
    9	Signature	nvarchar	8000	加密后的数据
    10	Create_Date	datetime	8	创建时间
    11	Modify_Date	datetime	8	修改时间
    12	Create_User_Id	bigint	8	创建者
    13	Modify_User_Id	bigint	8	修改者
    """

    origin_model = """
    order_id = models.BigIntegerField(db_column='Order_Id')  # Field name made lowercase.
    order_no = models.CharField(db_column='Order_No', max_length=32)  # Field name made lowercase.
    order_guid = models.CharField(db_column='Order_GUID', max_length=36)  # Field name made lowercase.
    buyer_user_id = models.BigIntegerField(db_column='Buyer_User_Id')  # Field name made lowercase.
    buyer_enterprise_id = models.BigIntegerField(db_column='Buyer_Enterprise_Id')  # Field name made lowercase.
    transaction_integral = models.BigIntegerField(db_column='Transaction_Integral')  # Field name made lowercase.
    earnest_integral = models.BigIntegerField(db_column='Earnest_Integral')  # Field name made lowercase.
    deduction_type = models.IntegerField(db_column='Deduction_Type', blank=True, null=True)  # Field name made lowercase.
    signature = models.TextField(db_column='Signature')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='Create_Date')  # Field name made lowercase.
    modify_date = models.DateTimeField(db_column='Modify_Date')  # Field name made lowercase.
    create_user_id = models.BigIntegerField(db_column='Create_User_Id')  # Field name made lowercase.
    modify_user_id = models.BigIntegerField(db_column='Modify_User_Id')  # Field name made lowercase.
    """
    holy = CreateModel(table_ds, origin_model)
    models = holy.holy_cow()
    # models = holy.beatify_model()
    print(models)

    with open('models.txt', 'a+', encoding='utf-8') as f:
        f.write(models)
