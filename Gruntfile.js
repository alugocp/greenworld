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
};
