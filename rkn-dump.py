
class RknDump:
    def __init__(self, filename = "dump.xml"):
        self.filename = filename;

    def getUpdateTime:
        s=ElementTree().parse(self.filename).attrib['updateTime']
        dt = datetime.strptime(ts[:19],'%Y-%m-%dT%H:%M:%S')
        return int(time.mktime(dt.timetuple()))+3

    def getUpdateTimeUrgently:
        pass

    def getFormatVersion:
        pass
