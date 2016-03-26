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
      dist: {
        files: {
          '<%= pkg.name %>/static/css/base.css': '<%= pkg.name %>/static/sass/base.scss',
          '<%= pkg.name %>/static/css/write.css': '<%= pkg.name %>/static/sass/write.scss'
        }
      }
    },

    postcss: {
      options: {
        processors: [
          require('pixrem')(),
          require('autoprefixer')(),
          require('cssnano')()
        ]
      },
      dist: {
        src: '<%= pkg.name %>/static/css/*.css'
      }
    },

    watch: {
      sass: {
        files: '<%= pkg.name %>/static/sass/*.scss',
        tasks: 'sass'
      }
    }
  });

  grunt.registerTask('local', ['sass', 'bgShell', 'watch']);
  grunt.registerTask('production', ['sass', 'postcss']);
  grunt.registerTask('default', ['production']);
};
