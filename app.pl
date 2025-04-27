# Code by Linus Wong 
# Comments by Tiffany Le 
# Date Created: 26 April 2025 
# Last Update: 8:48 pm 

use Dancer2;

get '/manifest.json' =>sub{
    send_file 'manifest.json';
}; 
set views => "ui";
set public_dir => ".";

hook before => sub {
    response_header 'Access-Control-Allow-Origin' => 'https://express.adobe.com';
    response_header 'Access-Control-Allow-Methods' => 'POST, GET, OPTIONS';
    response_header 'Access-Control-Allow-Headers' => 'Content-Type';
};

#set public_dir => "public";   # Static files
         # Templates (HTML)

# Home page with upload form
get '/' => sub {
    send_file 'index.html', system_path => 1;
};

# Handle file upload
post '/uploads/' => sub {
    # Verifies if file is updated 
    my $upload = upload('video');
    unless ($upload) {
        return "No video uploaded!";
    }
    # Concatenates uploads directory and file name 
    my $filename = 'uploads/' . $upload->filename;
    # Saves file to server 
    $upload->copy_to($filename);
    # test this 
    # print "Running transcribe on: $filename\n"; 

    # Call Python Whisper to transcribe
    my $output = `python3 backend/src/transcribe.py "$filename"`;

    # Returns formatted 
    #return "<h2>Transcription:</h2><pre>$output</pre>";
    # template 'results', { transcription => $output };
    my $html;
    {
    local $/;
    open my $fh, '<', 'results.html' or die "Could not open results.html: $!";
    $html = <$fh>;
    close $fh;
    }
    #my $html = slurp 'results.html'; 

    # Replace some special placeholder in your HTML
    $html =~ s/PLACEHOLDER_TRANSCRIPTION/$output/;

    return $html; 
};

start;
