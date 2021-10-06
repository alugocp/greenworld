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
    }
  });

  grunt.loadNpmTasks('grunt-tslint');
  grunt.loadNpmTasks('grunt-available-tasks');
  grunt.registerTask('default', ['availabletasks']);
};
