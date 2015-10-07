module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    bgShell: {
      serve: {
        bg: true,
        cmd: 'python <%= pkg.name %>/manage.py runserver'
      }
    },

    sass: {
      local: {
        options: {
          outputStyle: 'nested'
        },
        files: {
          '<%= pkg.name %>/static/css/base.css': '<%= pkg.name %>/static/sass/base.scss'
        }
      },
      production: {
        options: {
          outputStyle: 'compressed'
        },
        files: {
          '<%= pkg.name %>/static/css/base.css': '<%= pkg.name %>/static/sass/base.scss'
        }
      }
    },

    watch: {
      sass: {
        files: '<%= pkg.name %>/static/sass/*.scss',
        tasks: 'sass:local'
      }
    }
  });

  grunt.registerTask('local', ['sass:local', 'bgShell', 'watch']);
  grunt.registerTask('production', ['sass:production']);
  grunt.registerTask('default', ['production']);
};
