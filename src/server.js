const express = require('express');
const fs = require('fs');
const multer = require('multer');
let model = require('./model');

class Server {
  constructor() {
    let app = express();
    let self = this;
    const port = process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 8080;
    const ip = process.env.IP || process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
    app.use(express.static('public'));

    const upload = this._initMulter();

    app.post('/file_upload', function (req, res) {
      console.log('Response START');
      upload(req, res, function (err) {
        console.log(err);
        if (err) {
          let response = { msg: '', code: '' };
          if (err.code == 'LIMIT_FILE_SIZE') {
            response.msg =
              'File exceeds the limit ( ' +
              opts.limits.fileSize / 1024 / 1024 +
              'MB )';
            response.code = 'LIMIT_FILE_SIZE';
          } else if (err.code == 'NOT_ALLOWED_FORMAT') {
            response.msg = 'File format ( ' + err.format + ' ) not allowed';
            response.code = 'NOT_ALLOWED_FORMAT';
          } else {
            console.log('File Upload SYSTEM ERROR', err);
            response.msg = 'Server file upload system error';
            response.code = 'UPLOAD_SYSTEM_ERROR';
          }
          res.writeHead(500, {
            'Content-Type': 'application/json; charset=UTF-8',
          });
          res.end(JSON.stringify(response));
          return;
        }

        let fn = req.file.originalname;
        let extension = fn.substr(fn.lastIndexOf('.') + 1).toLowerCase();

        if (extension == 'obj') {
          model.objFileConvert(req.file.path);
          console.log('USE obj_fc');
        }

        fs.readFile(req.file.path, function (err, data) {
          console.log(req.file.path);
          console.log(err, data);
          fs.unlink(req.file.path, (err) => {
            if (err) throw err;
            console.log(req.file.path + ' was deleted');
          });
          if (err) {
            console.log('File reading SYSTEM ERROR', err);
            let response = {
              msg: 'Server file reading system error',
              code: 'READFILE_SYSTEM_ERROR',
            };
            res.writeHead(500, {
              'Content-Type': 'application/json; charset=UTF-8',
            });
            res.end(response);
          }
          if (data) {
            self.loadFileData(extension, data, function (obj_jr, status) {
              res.writeHead(status, {
                'Content-Type': 'application/json; charset=UTF-8',
              });
              res.end(JSON.stringify(obj_jr));
              console.log('Response DONE');
              if (global.gc) {
                global.gc();
              } else {
                console.log('Garbage collection unavailable.');
              }
            });
          }
        });
      });
    });

    app.listen(port, ip);
    console.log('Server running on http://%s:%s', ip, port);
  }

  _initMulter() {
    const suppFileE = [
      '3mf',
      'amf',
      'awd',
      'dae',
      'ctm',
      'stl',
      'obj',
      'ply',
      'vtk',
      'vtp',
    ];
    /**
     * 文件格式过滤器
     * @param {*} req
     * @param {*} file
     * @param {*} cb
     * @returns
     */
    let fileFilterF = function (req, file, cb) {
      let fn = file.originalname;
      let extension = '';
      let i = fn.lastIndexOf('.');
      if (i > 0) {
        extension = fn.substr(i + 1).toLowerCase();
        for (let j in suppFileE) {
          if (suppFileE[j] == extension) {
            cb(null, true);
            return;
          }
        }
      }
      cb(
        {
          Error: 'File format not support',
          code: 'NOT_ALLOWED_FORMAT',
          format: extension,
        },
        false
      );
    };

    let opts = {
      dest: 'uploads/',
      fileFilter: fileFilterF,
      limits: {
        fields: 0,
        fileSize: 31457280, //30MB Disc
        files: 1,
        parts: 1,
      },
    };

    let upload = multer(opts).single('file');
    this.upload = upload;
    return upload;
  }

  /**
   * load file data
   * @param {*} ext
   * @param {*} data
   * @param {*} method
   */
  loadFileData(ext, data, method) {
    let loader = require('./loader');
    try {
      loader.load(ext, data, function (backText) {
        method(backText, 200);
      });
    } catch (e) {
      console.log('THREE error', e);
      let response = {
        msg: 'Server system does not understand file content',
        code: 'READING_FILE_CONTENT_SYSTEM_ERROR',
      };
      method(response, 500);
    }
  }
}

new Server();
