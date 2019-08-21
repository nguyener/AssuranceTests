Rails.application.routes.draw do
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
  namespace :v1, defaults: {format: 'json'} do
    get 'boggle_game', to: 'boggle_game#index'
    get 'boggle_game/:word', to: 'boggle_game#checkWord'
  end

  get '*page', to: 'static#index', constraints: ->(req) do
    !req.xhr? && req.format.html?
  end
  root 'static#index'
end
