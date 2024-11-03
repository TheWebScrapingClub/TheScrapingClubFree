from scrapy.utils.project import get_project_settings
from scrapy.exporters import CsvItemExporter

class CsvItemExporter(CsvItemExporter):

	def __init__(self, *args, **kwargs):
		settings = get_project_settings()
		delimiter = settings.get('CSV_DELIMITER', ',')
		kwargs['delimiter'] = delimiter

		fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
		if fields_to_export :
			kwargs['fields_to_export'] = fields_to_export

		super(CsvItemExporter, self).__init__(*args, **kwargs)
