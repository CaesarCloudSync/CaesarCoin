const client = new WebTorrent();
const torrentId = "https://webtorrent.io/torrents/sintel.torrent"
client.add(torrentId, function (torrent) {
  // Torrents can contain many files. Let's use the .mp4 file
  const file = torrent.files.find(function (file) {
    return file.name.endsWith(".mp4");
  });
  console.log(file)

  // Render to a <video> element by providing an ID. Alternatively, one can also provide a DOM element.
  file.renderTo("video#video-container_html5_api", {}, () => {
    console.log("Ready to play!");
  });
});
/*    
<body>
    <h2>Todo</h2>
    <div ng-controller="TodoListController as todoList">
        <span>{{todoList.remaining()}} of {{todoList.todos.length}} remaining</span>
        [ <a href="" ng-click="todoList.archive()">archive</a> ]
        <ul class="unstyled">
        <li ng-repeat="todo in todoList.todos">
            <label class="checkbox">
            <input type="checkbox" ng-model="todo.done">
            <span class="done-{{todo.done}}">{{todo.text}}</span>
            </label>
        </li>
        </ul>
        <form ng-submit="todoList.addTodo()">
        <input type="text" ng-model="todoList.todoText"  size="30"
                placeholder="add new todo here">
        <input class="btn-primary" type="submit" value="add">
        </form>
    </div>
    </body> */
/*
angular.module('todoApp', [])
.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [
    {text:'learn AngularJS', done:true},
    {text:'build an AngularJS app', done:false}];
    todoList.addTodo = function() {
    todoList.todos.push({text:todoList.todoText, done:false});
    todoList.todoText = '';
    };
    todoList.remaining = function() {
    var count = 0;
    angular.forEach(todoList.todos, function(todo) {
        count += todo.done ? 0 : 1;
    });
    return count;
    };
    todoList.archive = function() {
    var oldTodos = todoList.todos;
    todoList.todos = [];
    angular.forEach(oldTodos, function(todo) {
        if (!todo.done) todoList.todos.push(todo);
    });
    };
});


 */
