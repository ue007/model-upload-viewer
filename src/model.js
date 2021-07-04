const fs = require('fs');

module.exports = {
  objFileConvert: function (filePath) {
    let st = fs.readFileSync(filePath) + '';
    let lines = st.split('\n');
    let text = '';
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      let line0C = line.charAt(0);
      let line1C = line.charAt(1);

      if (line0C == 'v' && line1C == ' ') {
        text += line + '\n';
      }

      if (line0C == 'f' && line1C == ' ') {
        let t = 'f';

        if (line.indexOf('/') == -1) {
          text += line + '\n';
        } else {
          let s = line.split(' ');
          for (let j = 1; j < s.length; j++) {
            t += ' ' + s[j].substr(0, s[j].indexOf('/'));
          }
          text += t + '\n';
        }
      }
    }

    try {
      fs.truncateSync(filePath, 0);
      fs.writeFileSync(filePath, text);
    } catch (e) {
      console.log('ERROR .obj FileConvert');
    }
  },
};
