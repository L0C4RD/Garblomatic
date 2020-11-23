
# Garblomatic

A simple Google-assisted tool for garbling text.

## What does this tool do?

Garblomatic takes the contents of a text file, and recursively passes it through the Google Translate API. You can tell Garblomatic which translation settings you'd like it to use along the way, or simply let it pick a few at random. It's written for Python 3.7, and doesn't have any other dependencies beyond that.

It is based on @JKomskis ' excellent [Google Garbler](https://github.com/JKomskis/GoogleGarbler) project, but streamlined for execution on a local machine.

## Usage

To garble the contents of a text file using default settings, simply run:

```bash
./garble.py my_file.txt
```

You can specify settings in a number of ways. By default, the text file is translated through three randomly-selected languages. To specify the number of randomly-selected languages, use the `-r` flag:

```bash
./garble.py -r 5 my_file.txt
```

You can also specify precisely which languages you'd like to use. To do so, simply list any number of languages (in order) at the end of the command:

```bash
./garble.py my_file.txt afrikaans albanian amharic
```

If you'd like to see a list of supported languages, use the `-l` flag:

```bash
./garble.py -l
```

## Other settings

By default, Garblomatic assumes that the text you wish to garble has been authored in the English langage. To specify a different base language, use the `-b` flag:

```bash
./garble.py -b french my_file.txt
```

If you'd like Garblomatic to output to a file instead of stdout, you can specify the path of this file using the `-o` flag:

```bash
./garble.py -o garbled_file.txt my_file.txt
```

Similarly, if you wish to pipe input to Garblomatic via stdin rather than via an input file, you can do so using the `-s` flag:

```bash
echo "Here's some text" | ./garble.py -s 
```

### Enjoy!
