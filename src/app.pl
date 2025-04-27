# Code by Linus Wong 
# Comments by Tiffany Le 
# Date Created: 26 April 2025 
# Last Update: 8:48 pm 

use Dancer2;

set public_dir => "public";   # Static files
set views => "index";         # Templates (HTML)

# Home page with upload form
get '/' => sub {
    template 'index';
};

# Handle file upload
post '/upload' => sub {
    # Verifies if file is updated 
    my $upload = upload('file');
    unless ($upload) {
        return "No file uploaded!";
    }
    # Concatenates uploads directory and file name 
    my $filename = 'uploads/' . $upload->filename;
    # Saves file to server 
    $upload->copy_to($filename);

    # Call Python Whisper to transcribe
    my $output = 'python3 transcribe.py $filename';

    # Returns formatted 
    return "<h2>Transcription:</h2><pre>$output</pre>";
};

start;
