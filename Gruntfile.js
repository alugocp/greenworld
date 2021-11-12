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
          'tests/*.spec.ts',
          'tasks/lib/*.ts',
          'tasks/*.ts'
        ]
      }
    },
    availabletasks: {
      tasks: {}
    },
    ts: {
      default : {
        tsconfig: 'tsconfig.json'
      }
    },
    run: {
      evaluate: {
        cmd: 'node',
        args: [
          'build/evaluate.js'
        ]
      },
      uptake: {
        cmd: 'node',
        args: [
          'build/uptake.js'
        ]
      },
      test: {
        cmd: 'ts-mocha',
        args: [
          'tests/*.spec.ts'
        ]
      }
    }
  });

  // Loaded NPM tasks
  grunt.loadNpmTasks('grunt-ts');
  grunt.loadNpmTasks('grunt-run');
  grunt.loadNpmTasks('grunt-tslint');
  grunt.loadNpmTasks('grunt-available-tasks');

  // Aliased tasks
  grunt.registerTask('lint', ['tslint']);
  grunt.registerTask('default', ['availabletasks']);
  grunt.registerTask('evaluate', ['run:evaluate']);
  grunt.registerTask('uptake', ['run:uptake']);
  grunt.registerTask('test', ['run:test']);
  grunt.registerTask('qualify', ['lint', 'test']);
};
