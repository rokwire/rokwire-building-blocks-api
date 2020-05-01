import os
import shutil
import tempfile
import controllers.configs as cfg


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in cfg.ALLOWED_EXTENSIONS


def savefile(file, filename):
    try:
        _, tmpfolder = os.path.split(tempfile.mkdtemp())
        tmpfolder = cfg.IMAGE_FILE_MOUNTPOINT + tmpfolder
        os.mkdir(tmpfolder)
        tmpfile = tmpfolder + "/" + filename
        file.save(tmpfile)
    except Exception as ex:
        raise
    return tmpfile


def deletefile(tmpfile):
    try:
        if os.path.exists(tmpfile):
            tmpfolder, _ = os.path.split(tmpfile)
            shutil.rmtree(tmpfolder)
    except Exception as ex:
        pass
