#!/usr/bin/env python
# encoding: utf-8

from revue import app

if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOSTNAME'])
