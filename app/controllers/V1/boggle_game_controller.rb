require 'rest-client'
class V1::BoggleGameController < ApplicationController
  $rows = 4
  $cols = 4
  $gameBoard = Array.new($rows) { Array.new($cols) }

  def index
    $gameBoard.each do |row|
      $gameBoard.each_with_index do |x, xi|
        x.each_with_index do |y, yi|
          $gameBoard[xi][yi] = {letter: ('A'.ord + rand(25)).chr, selected: false}
        end
      end
    end

    render json: {:gameBoard => $gameBoard
    }.to_json
  end

  def checkWord
    wordToCheck = params['word']
    url = "https://wordsapiv1.p.rapidapi.com/words/" + wordToCheck + "/definition"
    response = RestClient::Request.execute(
        method: :get,
        url: url,
        headers: {
            "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
            "x-rapidapi-key": "9ca4422241mshe0286c9a9674497p14d0e5jsn7d6a927fd826"
        }
    )
    render json: {valid:true, word:wordToCheck}.to_json
  rescue RestClient::Exception
      render json: {valid:false, word: wordToCheck}.to_json
  end
end
