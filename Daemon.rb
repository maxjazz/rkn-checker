private

def daemonize(pathStdErr, oldmode=0, closefd=false)
  srand # Split rand streams between spawning and daemonized process
    safefork and exit# Fork and exit from the parent

    # Detach from the controlling terminal
    unless sess_id = Process.setsid
        raise 'Cannot detach from controlled terminal'
    end

    # Prevent the possibility of acquiring a controlling terminal
    if oldmode.zero?
        trap 'SIGHUP', 'IGNORE'
        exit if pid = safefork
    end

    Dir.chdir "/"   # Release old working directory
    File.umask 0000 # Insure sensible umask

    if closefd
        # Make sure all file descriptors are closed
        ObjectSpace.each_object(IO) do |io|
            unless [STDIN, STDOUT, STDERR].include?(io)
                io.close rescue nil
            end
        end
    end

    STDIN.reopen "/dev/null"       # Free file descriptors and
    STDOUT.reopen "/dev/null"   # point them somewhere sensible
    STDERR.reopen pathStdErr, "w"           # STDOUT/STDERR should go to a logfile
    return oldmode ? sess_id : 0   # Return value is mostly irrelevant
end
