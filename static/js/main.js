require.config({
    shim: {
        'underscore': {
            exports: '_'
        },
        'handlebars': {
            exports: 'Handlebars'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    },
    paths: {
        'jquery': 'jquery-2.0.0.min',
        'backbone': 'backbone-min',
        'underscore': 'underscore-min',
        'handlebars': 'handlebars',
        'backbone_poller': 'backbone.poller.min',
    }
});

require(['App'], function(App){
    $(function(){
        var task_id = '',
            $task_info = $('#task-info');
        if ($task_info.length){
            task_id = $.parseJSON($task_info.html()).task_id;
        }
        console.log('current task_id', task_id);
        new App($('#task'), task_id);
    });
});
