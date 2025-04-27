use Dancer2;

set public_dir => "public";   # Static files
set views => "index";         # Templates (HTML)

#Home page with upload form
get '/' => sub {
    template 'index';
};

#Handle file upload
post '/upload' => sub {
    my $upload = upload('file');
    unless ($upload) {
        return "No file uploaded!";
    }
    my $filename = 'uploads/' . $upload->filename;
    $upload->copy_to($filename);

    # Call Python Whisper to transcribe
    my $output = 'python3 transcribe.py $filename';

    return "<h2>Transcription:</h2><pre>$output</pre>";
};

start;
