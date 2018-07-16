class DefaultConfig(dict):
	def __init__(self):
		# ------------ 数据路径 ------------
		
		self['data_dir'] = '../../MOBIKE_CUP_2017'
		self['train_csv'] = self['data_dir'] + '/train.csv'
		self['test_csv'] = self['data_dir'] + '/test.csv'
		self['cache_dir'] = '../cache'
		self['model_dir'] = '../snapshot'
		self['result_dir'] = '../result'

		# ------------ 训练参数 --------

		self['startday'] = 23
		self['endday'] = 25
		self['lgb_leaves'] = 96
		self['lgb_lr'] = 0.05

		# ------------ 测试参数 --------

		self['test_startday'] = 25
		self['test_endday'] = 26
		self['model_name'] = None
        
		# -------- 是否有用户 --------
        
		self['user'] = True

	def update(self, **kwargs):
		for key in kwargs:
		    self[key] = kwargs[key]
		self['time_prefix'] = '2017-05-'
		self['time_suffix'] = ' 00:00:00'
		self['starttime'] = '2017-05-' + str(self['startday']) + ' 00:00:00'
		self['endtime'] = '2017-05-' + str(self['endday']) + ' 00:00:00'
		self['test_starttime'] = '2017-05-' + str(self['test_startday']) + ' 00:00:00'
		self['test_endtime'] = '2017-05-' + str(self['test_endday']) + ' 00:00:00'

	def printf(self):
		print('Current Config:')
		for key in self:
			print('{}: {}'.format(key, self[key]))
