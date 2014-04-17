#!/usr/bin/env ruby

## Get the git log from components list
## two use mode, detect git repo automatically
## and specify with component list

require 'date'
require 'optparse'

class GitStat
  attr_reader :changes

  def initialize(repos, output)
    puts repos
    @repos = repos
    @output = output
    @changes = []
    detect_gits() if @repos == nil
  end

  def sha(commit)
    commit.split(" ")[1]
  end

  def detect_gits()
    puts "detect_gits"
  end

  def process(repo)
    Dir.chdir(repo) do
      puts "process #{repo}"
      log = `git log`
      commits = log.split("\n").reject! { |l|
        l.index("commit") != 0
      }
      commits.reverse!
      commits.each_with_index { |commit, index|
        break if index >= commits.size() - 1
        log = `git log #{sha(commit)}..#{sha(commits[index+1])} --numstat`
        if log != nil and log.size() != 0
          author, time, add, sub =  diff(log)
          line = "#{author}\t#{time}\t#{add}\t#{sub}\n"
          @changes << [author, time, add, sub, repo]
        end
      }
    end
  end

  def diff(log)
    lines = log.split("\n")
    author = lines.reject { |l| l.index("Author:") != 0 }
    author = author[0].split()[1]
    author.capitalize!

    time = lines.reject { |l|  l.index("Date:") != 0 }
    time = time[0].gsub("Date:", "").gsub("+0800", "").strip()

    diffline = lines.select { |l|
        (l =~ /^\d/) and
        (l =~ /.[hh|cc|c|h|mk|py|gitignore]$/) and
        (not l =~ /\.in$/)
    }
    add = sub = 0
    diffline.each { |l|
      elems = l.split()
      add += elems[0].to_i
      sub += elems[1].to_i
    }
    time = DateTime.strptime(time, '%a %b %d %H:%M:%S %Y')
    return author, time, add, sub
  end

  def run()
    result = []
    @repos.each { |r|
      process(r)
    }
    ## sort with time
    @changes.sort! { |x, y|
      x[1] <=> y[1]
    }

    fp = File.open(@output, "w+")
    @changes.each { |l|
      author, time, add, sub, comp = l[0], l[1], l[2], l[3], l[4]
      fp.write("#{author}\t#{time}\t#{add}\t#{sub}\t#{comp}\n")
    }
    fp.close()
  end
end

options = {}
option_parser = OptionParser.new do |opts|
  opts.banner = 'gitstat.rb, a utility to get git commits log from components'

  opts.on('-o NAME', '--out Name', 'Set log into output file NAME') do |value|
    options[:output] = value
  end

  opts.on('-l COMP_A COMP_B', '--list COMP_A COMP_B', Array,'Set the component list') do |value|
    options[:dirs] = value
  end
end.parse!

puts options.inspect
stat = GitStat.new(options[:dirs], options[:output])
stat.run()
