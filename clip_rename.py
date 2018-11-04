import re
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

_CLIPS_FOLDER_ID="0B1R0H7mMyvBmbGFGRGdMOGZ1RTg"
_CLIP_NAME_REGEX="^Clip \((?P<month>\w+) (?P<day>\d+) (?P<year>\d+) at (?P<hhmm>\d+) (?P<meridian>\w+)\).mp4$"


def ClipToDateTime(title):
    m = re.search(_CLIP_NAME_REGEX, title)
    if m:
        d = m.groupdict()
        sane_datetime_string = "%s %02d %04d %04d %s" % (d['month'], int(d['day']), int(d['year']), int(d['hhmm']), d['meridian'])
        return datetime.strptime(sane_datetime_string, "%B %d %Y %I%M %p")
    

def main():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({
        'q' : "'%s' in parents" % _CLIPS_FOLDER_ID}).GetList()
    for file1 in file_list:
        title = file1['title']
        id_ = file1['id']
        print('title: {}, id: {}'.format(title, id_))
        dt = ClipToDateTime(title)
        if dt:
            print "%s to %s" % (title, dt)
            file1['title']=("%s" % dt)
            file1.Upload()

if __name__ == '__main__':
    main()
