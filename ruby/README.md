# Get started

Requires Ruby 1.9+. Tested with Ruby 2.2.4 and Ruby 1.9.3. Also requires [Bundler](http://bundler.io/).

```bash
bundle install --path vendor
```

# Run the tests

```bash
bundle exec rspec spec/scrabble_spec.rb
```

# Files

- `spec/scrabble_spec.rb`: The tests for the Scrabble logic.
- `scrabble.rb`: Where you need to implement the game's logic to make the tests pass.
- `dictionary.rb`: A helper to test if a word is valid.
