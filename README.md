# Nots: an ORM for your shell

## Getting Started

### Setting up Nots

1. Clone this repository into a directory of your choosing.
2. In this directory, run `./bin/setup`.
3. Initialize `nots` by running `nots setup system`.

### Creating Your First Resource

Todos are the Hello Worlds of programming projects, so let's get started with a project that allows us to list a bunch
of items we have to take care off.

Let's begin by creating a new resource. In traditional terms a resource is a _record_. In webscale terms this might be
called a _document_.

```shell
nots create resource --name=todo --plural=todos
```

We can verify that `nots` has created our resource by running `nots list resources`. This will produce the following
output:

```
NAME         PLURALITY    TABLE
todo         todos        todo
```

With our resource created we must let `nots` know what kind of fields our resource can expect. A field in traditional
terms is a column, in modern terms you might call it a "key". When creating a field for a resource you need to at least
specify a name, optionally are the type, and a default value. If you do not specify a default value then the field
becomes required. if you do not specify a type then the type will become `text`.

```shell
nots create field --resource=todo --name=description
```

Again we can confirm that our field has been created by running `nots list fields --resource=todo`. The output will look
something like this:

```
NAME          TYPE         DEFAULT      RESOURCE
description   text         None         todo
```

You might recall that you've also specified the plural term for your resources, you can use this too! Go ahead and run
`nots list fields --resource=todos` and you'll see identical output.

Now that we can store a description, we should also add a field that shows whether the task is done or not. Let's call
the field
`done` with type `boolean`. Nots has only a few built-in types which we'll cover later.

```shell
nots create field --resource=todo --name=done --type=boolean --default=false
```

Again we can inspect our resource by running `nots list fields --resource=todo`:

```
NAME          TYPE         DEFAULT      RESOURCE
description   text         None         todo
done          boolean      false        todo
```

Now that we have the fields needed, let's begin by creating our first `todo` record!

```shell
nots create todo --description="Learn more about all the things I can do with nots"
```

I hope you're not lactose intolerant, because we're also going to buy some milk.

```shell
nots create todo --description="Buy two cartons of milk"
```

Wow, we created two records, and I already forgot what the first item was. What good would `nots` be if we couldn't find
our records again.

```shell
nots list todos
```

This should give you the following output.

```
ID           DESCRIPTION                                          DONE
1            Learn more about all the things I can do with nots   False
2            Buy two cartons of milk                              False
```

That's great! If you feel like you learned about all the things you can do with `nots` (you didn't), go ahead and mark
the task as done.

```shell
nots update todo --done=true --id__eq=1
```

Here the ORM magic of `nots` hopefully starts the shine. We've specified the field we want to update by simply
specifying it as `--done=true`, but we were also able to select with `--id__eq`. There's some more operators such
as `__neq`, `__gt`, `__gte`, `__lt`, and `__lte`. These operators are described somewhere else in this README.

Now if we list our resources, we'll see:

```
ID           DESCRIPTION                                          DONE
1            Learn more about all the things I can do with nots   True
2            Buy two cartons of milk                              False
```

Querying does not only work with updating, it also works with listing. For example if we want to list our tasks that are
done we can run `nots list todos --done__eq=true`

```
ID           DESCRIPTION                                          DONE
1            Learn more about all the things I can do with nots   True
```

Of course, we can list our pending items by running `nots list todos --done__eq=false`. If feel it you can of course
also query for the inverse: `nots list todos --done__neq=true`. All fields, except for `id`, can be updated, and you can
update one, or all fields, in a single operation.

```shell
nots update todo --done=True --description="Buy one carton of milk" --id__eq=2
```

By now you probably have a good idea on how to get, create, and update resources. There is one more remaining, which is
deletion of a resource. Let's remove task with `id` `2`.

```shell
nots delete todo --id__eq=2
```

Go ahead and list your todos, you'll see it's now gone:

```
ID           DESCRIPTION                                          DONE
1            Learn more about all the things I can do with nots   True
```

One last thing, so far you've output the data only to a table. This is easy for you, but perhaps not ideal if you want
to pipe `nots` output to other processes. You can change the output mode to `json` by adding `--output=json` to your
list operation. For example `nots list todos --output=json` will generate the following output:

```json
[
  {
    "id": 1,
    "description": "Learn more about all the things I can do with nots",
    "done": true
  }
]
```

If you don't want certain fields, for example you wish to omit id, you can specify the fields you want to output by
specifying `--fields`. In our example with `todo` resources we can
run `nots list todos --output=json --fields=description,done`
which will output the following:

```json
[
  {
    "description": "Learn more about all the things I can do with nots",
    "done": true
  }
]
```

This works with all output modes, so by omitting the output mode you'll get the following result:

```
DESCRIPTION                                          DONE
Learn more about all the things I can do with nots   True
```

### What's next?

Nots does storing and querying data pretty well, but like all databases it needs to be wrapped to be truly convenient.
It's up to you, as a developer, to make this happen!

For example, I use the following shell function to manage my todo list:

```shell
#!/usr/bin/env bash

todo() {

  if [ "$1" = "list" ]; then
    nots list todos
  fi

  if [ "$1" = "list-done" ]; then
    nots list todos --done__eq=true
  fi

  if [ "$1" = "list-todo" ]; then
    nots list todos --done__eq=false
  fi

  if [ "$1" = "mark-done" ]; then
    nots update todos --done=true --id__eq="$2"
  fi

  if [ "$1" = "add" ]; then
    nots create todo --description="$2"
  fi

}
```

This allows me to run commands like `todo list`, `todo list-todo`, `todo list-todo`, `todo mark-done 1`
, and `todo add "Get help with my milk addiction."`

## Requirements

* Python 3.6 with `venv` support.

## Types

Because `nots` is using Sqlite as a backend, types are few:

* datetime
* text
* int
* float
* boolean

## Special Defaults

You can specify special default values, `nots` currently supports the following special defaults:

* `NOW` -- inserts the current time.
* `UUID` -- inserts a uuid v4.

You can use defaults in the following manner:

```shell
nots create field --name=myfield --type=datetime --default=NOW
```

Make sure you match the types. Although you can use `NOW` with `--type=text` it pays to use `--type=datetime`.

## Query Operators

* `__eq` `a = b`
* `__neq` `a != b`
* `__gt` `a > b`
* `__gte` `a >= b`
* `__lt` `a < b`
* `__lte` `a <= b`

## Things it can't do (yet)

* Foreign Keys
* Support for databases other than SQLite
* `__in` operators.

## How does it work?

Nots uses Sqlite as a persistent backend for storing data. All operations follow the same format:

```shell
nots verb resource --parameters
```

Nots then turns these parameters into queries using SQLAlchemy.

## It doesn't work.

Run your command with `-v3` to spit out debug information, copy and paste the entire output into a new GitHub issue and
we'll look at it, probably.

## Infrequently Asked Questions

### What does Nots mean?

It's like notes, but then `nots`. As in, "Hey papi mak me sum `nots`."

### Does Nots support any other backend than Sqlite?

No, not at this time but implementing this functionality should be pretty easy.