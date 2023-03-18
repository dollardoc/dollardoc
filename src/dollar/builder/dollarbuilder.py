from dollar.confighandler import ConfigHandler
from dollar.dollarobjectidmap import DollarObjectIdMap
from dollar.dollarobjectimpl import DollarObjectImpl
from dollar.file.dollarfile import DollarFile
from dollar.file.dollarfilereader import DollarFileReader
from dollar.file.dollarfilewriter import DollarFileWriter
from dollar.format.header.headerparser import HeaderParser
from dollar.format.raw.rawdollarparser import RawDollarParser
from dollar.format.transformer.headertransformer import HeaderTransformer
from dollar.format.transformer.inputtostrtransformer import InputToStrTransformer
from dollar.format.transformer.rawtoinputtransformer import RawToInputTransformer
from dollar.plugin.builtinpluginloader import BuiltinPluginLoader
from dollar.plugin.pluginhandler import PluginHandler
from dollar.plugin.pluginmap import PluginMap


class DollarBuilder:

    @staticmethod
    def build():
        ConfigHandler.load_config_default()
        BuiltinPluginLoader.load()
        PluginHandler.importplugins(
                ConfigHandler.get("plugin_path"))

        mdd_files = DollarFileReader.read_mdd_files(
                ConfigHandler.get("docs_path"))

        dollar_object_list = []

        for mdd_file in mdd_files:
            path = mdd_file.getpath()
            content = mdd_file.getcontent()

            dollar_object = DollarObjectImpl(
                    content,
                    path,
                    path[:-1],
                    "/" + path[:-1].replace("\\", "/"))

            header_parser_result = HeaderParser.parse(content)
            dollar_object.setunparsedheader(header_parser_result.header_object)
            dollar_object.setheaderend(header_parser_result.header_end)

            DollarObjectIdMap.add(dollar_object)
            dollar_object_list.append(dollar_object)

        for dollar_object in dollar_object_list:
            dollar_object.setheader(
                    HeaderTransformer.transform(dollar_object, dollar_object.getunparsedheader()))

            PluginMap.getextension(dollar_object.gettype())\
                    .execprimary(dollar_object)

            for key in dollar_object.getheader().keys():
                if PluginMap.hasextensionwithsecondarykey(key):
                    PluginMap.getextensionfromsecondarykey(key)\
                            .execsecondary(dollar_object)

        for dollar_object in dollar_object_list:
            dollar_object.setrawformats(
                    RawDollarParser.parse(dollar_object.getcontentwithoutheader()))

        for dollar_object in dollar_object_list:
            dollar_object.setinputformats(
                    RawToInputTransformer.transform_list(dollar_object, dollar_object.getrawformats()))

        for dollar_object in dollar_object_list:
            dollar_object.setoutput(
                    InputToStrTransformer.transform_list(dollar_object, dollar_object.getinputformats()))

        outputs = []
        for dollar_object in dollar_object_list:
            dollar_file = DollarFile(
                    dollar_object.getoutputpath(),
                    dollar_object.getoutput())
            outputs.append(dollar_file)
        DollarFileWriter.write_files(outputs)