module.exports = function(grunt) {

  grunt.initConfig({
    tslint: {
      options: {
        configuration: 'tslint.json',
        force: true,
        fix: false
      },
      files: {
        src: [
          'Gruntfile.js',
          'src/**/*.ts'
        ]
      }
    },
    availabletasks: {
      tasks: {}
    },
    run: {
      compile: {
        cmd: 'tsc',
        args: ['-p', 'tsconfig.json']
      },
      evaluate: {
        cmd: 'node',
        args: ['build/tasks/evaluate.js']
      },
      info: {
        cmd: 'node',
        args: ['build/tasks/info.js']
      },
      test: {
        cmd: 'ts-mocha',
        args: ['src/tests/*.spec.ts']
      }
    }
  });

  // Loaded NPM tasks
  grunt.loadNpmTasks('grunt-run');
  grunt.loadNpmTasks('grunt-tslint');
  grunt.loadNpmTasks('grunt-available-tasks');

  // Aliased tasks
  grunt.registerTask('lint', ['tslint']);
  grunt.registerTask('default', ['availabletasks']);
  grunt.registerTask('evaluate', ['run:evaluate']);
  grunt.registerTask('compile', ['run:compile']);
  grunt.registerTask('info', ['run:info']);
  grunt.registerTask('test', ['run:test']);
  grunt.registerTask('verify', ['lint', 'compile', 'test']);
};
